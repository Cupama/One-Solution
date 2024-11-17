odoo.define("pos_customizations.RefundButton", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const RefundButton = require("point_of_sale.RefundButton");
    const rpc = require('web.rpc');

    const PosRefundButtonCustom = (RefundButton) =>
        class extends RefundButton {
            setup() {
                super.setup();
                debugger;
                this.isHidden = false;
                const userId = this.env.pos.user.id
                rpc.query({
                    model: 'res.users',
                    method: 'check_cashier_group',
                    args: [userId],
                }).then((hasGroup) => {
                    this.isHidden = !hasGroup;
                    if (this.isHidden) {
                        this.el.style.display = 'none';
                    } else {
                        this.el.style.display = '';
                    }
                });
                rpc.query({
                    model: 'res.users',
                    method: 'has_group',
                    args: ['pos_customizations.group_allow_backend'],
                }).then((hasGroup) => {
                    if (hasGroup) {
                        this.env.pos.user.is_hidden = 1;
                    } else {
                        this.env.pos.user.is_hidden = 0;
                    }
                });
            }
        };
    Registries.Component.extend(RefundButton, PosRefundButtonCustom);
    return RefundButton;
});
