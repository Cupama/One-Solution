from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    pos_conf_id = fields.Many2one(
        'pos.config',
        string="Select POS",
        help='Point of Sale opened automatically for this user after login.',
    )
