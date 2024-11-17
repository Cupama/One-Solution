from odoo import fields, models, api
from odoo.http import request


class ResUsers(models.Model):
    _inherit = "res.users"

    pos_conf_id = fields.Many2one('pos.config', string="Select POS", help='select POS for the user')

    @api.model
    def check_cashier_group(self, user_id=None):
        if user_id:
            user = self.env['res.users'].browse(user_id)
            if user and user.has_group('pos_customizations.group_allow_refund'):
                return True
        return False