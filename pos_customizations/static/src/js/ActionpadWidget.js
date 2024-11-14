odoo.define('pos_customizations.ActionpadWidget', function (require) {
    'use strict';

    const ActionpadWidget = require('point_of_sale.ActionpadWidget');
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');

    const CustomActionpadWidget = (ActionpadWidget) =>
        class extends ActionpadWidget {
            get isLongName() {
                this.isHidden = false;
                const user = this.env.pos.user.id
                if (this.props.actionName && this.props.actionName.toLowerCase() === 'refund') {
                    rpc.query({
                        model: 'res.users',
                        method: 'check_cashier_group',
                        args: [user],
                    }).then((hasGroup) => {
                        this.isHidden = !hasGroup;
                        if (this.isHidden) {
                            this.el.style.display = 'none';
                        } else {
                            this.el.style.display = '';
                        }
                    });
                }
                return this.props.partner && this.props.partner.name.length > 10;
            }
        };

    Registries.Component.extend(ActionpadWidget, CustomActionpadWidget);
    return ActionpadWidget;
});
