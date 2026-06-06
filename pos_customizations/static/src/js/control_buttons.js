/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { user } from "@web/core/user";
import { useState } from "@odoo/owl";

/**
 * Hide the "Refund" control button from users that are not allowed to refund.
 * Only members of `pos_customizations.group_allow_refund` may see it.
 *
 * The group check is asynchronous, so the result is stored in a reactive state
 * that the inherited template reads (`refundAccess.allowed`).
 */
patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        this.refundAccess = useState({ allowed: false });
        user.hasGroup("pos_customizations.group_allow_refund").then((hasGroup) => {
            this.refundAccess.allowed = hasGroup;
        });
    },
});
