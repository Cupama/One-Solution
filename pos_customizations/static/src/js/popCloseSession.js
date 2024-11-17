odoo.define('pos_customizations.ClosePosPopup', function (require) {
    'use strict';

    const ClosePosPopup = require('point_of_sale.ClosePosPopup');
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');

    const CustomClosePosPopup = (ClosePosPopup) =>
        class extends ClosePosPopup {
            async closeSession() {
            if (!this.closeSessionClicked) {
                this.closeSessionClicked = true;
                await this.env.pos.push_orders_with_closing_popup();
                if (this.cashControl) {
                    const response = await this.rpc({
                        model: 'pos.session',
                        method: 'post_closing_cash_details',
                        args: [this.env.pos.pos_session.id],
                        kwargs: {
                            counted_cash: this.state.payments[this.defaultCashDetails.id].counted,
                        },
                    });
                    if (!response.successful) {
                        return this.handleClosingError(response);
                    }
                }
                await this.rpc({
                    model: 'pos.session',
                    method: 'update_closing_control_state_session',
                    args: [this.env.pos.pos_session.id, this.state.notes],
                });

                try {
                    const bankPaymentMethodDiffPairs = this.otherPaymentMethods
                        .filter((pm) => pm.type === 'bank')
                        .map((pm) => [pm.id, this.state.payments[pm.id].difference]);
                    const response = await this.rpc({
                        model: 'pos.session',
                        method: 'close_session_from_ui',
                        args: [this.env.pos.pos_session.id, bankPaymentMethodDiffPairs],
                        context: this.env.session.user_context,
                    });

                    if (!response.successful) {
                        return this.handleClosingError(response);
                    }
                    rpc.query({
                        model: 'res.users',
                        method: 'has_group',
                        args: ['pos_customizations.group_allow_backend'],
                    }).then((hasGroup) => {
                        if (hasGroup) {
                            window.location = '/web#action=point_of_sale.action_client_pos_menu';
                        } else {
                            window.location = '/web/session/logout';
                        }
                    });

                } catch (error) {
                    const iError = identifyError(error);
                    if (iError instanceof ConnectionLostError || iError instanceof ConnectionAbortedError) {
                        await this.showPopup('ErrorPopup', {
                            title: this.env._t('Network Error'),
                            body: this.env._t('Cannot close the session when offline.'),
                        });
                    } else {
                        await this.showPopup('ErrorPopup', {
                            title: this.env._t('Closing session error'),
                            body: this.env._t(
                                'An error occurred while trying to close the session.\n' +
                                'Redirecting to the back-end to manually close the session.'
                            ),
                        });
                        window.location = '/web#action=point_of_sale.action_client_pos_menu';
                    }
                }
                this.closeSessionClicked = false;
            }
        }
    };

    Registries.Component.extend(ClosePosPopup, CustomClosePosPopup);
    return ClosePosPopup;
});
