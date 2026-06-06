/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ClosePosPopup } from "@point_of_sale/app/components/popups/closing_popup/closing_popup";
import { ConnectionLostError } from "@web/core/network/rpc";
import { parseFloat } from "@web/views/fields/parsers";
import { user } from "@web/core/user";
import { useState } from "@odoo/owl";

/**
 * Locked-down kiosk behaviour for the closing popup:
 *  - Managers (`group_allow_backend`) get a "Backend" button to leave the POS
 *    while keeping the session open, and are redirected to the backend once the
 *    session is closed.
 *  - Cashiers (no backend access) are logged out as soon as the session closes,
 *    so the terminal is ready for the next user instead of falling back to the
 *    POS login screen.
 *
 * `closeSession` mirrors the standard Odoo 19 implementation and only changes
 * the redirection performed on a successful close.
 */
patch(ClosePosPopup.prototype, {
    setup() {
        super.setup();
        this.backendAccess = useState({ allowed: false });
        user.hasGroup("pos_customizations.group_allow_backend").then((hasGroup) => {
            this.backendAccess.allowed = hasGroup;
        });
    },

    async closeSession() {
        this.pos._resetConnectedCashier();
        // If there are orders in the db left unsynced, we try to sync.
        const syncSuccess = await this.pos.pushOrdersWithClosingPopup();
        if (!syncSuccess) {
            return;
        }
        if (this.pos.config.cash_control) {
            const response = await this.pos.data.call(
                "pos.session",
                "post_closing_cash_details",
                [this.pos.session.id],
                {
                    counted_cash: parseFloat(
                        this.state.payments[this.props.default_cash_details.id].counted
                    ),
                }
            );

            if (!response.successful) {
                return this.handleClosingError(response);
            }
        }

        try {
            await this.pos.data.call("pos.session", "update_closing_control_state_session", [
                this.pos.session.id,
                this.state.notes,
            ]);
        } catch (error) {
            // We have to handle the error manually otherwise the validation check stops the script.
            if (!error.data && error.data.message !== "This session is already closed.") {
                throw error;
            }
        }

        try {
            const bankPaymentMethodDiffPairs = this.props.non_cash_payment_methods
                .filter((pm) => pm.type == "bank")
                .map((pm) => [pm.id, this.getDifference(pm.id)]);
            const response = await this.pos.data.call(
                "pos.session",
                "close_session_from_ui",
                [this.pos.session.id, bankPaymentMethodDiffPairs],
                {
                    context: {
                        device_identifier: this.pos.device.identifier,
                    },
                }
            );
            if (!response.successful) {
                return this.handleClosingError(response);
            }
            this.pos.session.state = "closed";
            // Custom redirect: managers go to the backend, cashiers are logged out.
            if (this.backendAccess.allowed) {
                this.pos.redirectToBackend();
            } else {
                window.location = "/web/session/logout";
            }
        } catch (error) {
            if (error instanceof ConnectionLostError) {
                throw error;
            } else {
                await this.handleClosingControlError();
            }
        } finally {
            localStorage.removeItem(`pos.session.${odoo.pos_config_id}`);
        }
    },
});
