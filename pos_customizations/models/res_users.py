from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    pos_conf_id = fields.Many2one('pos.config', string="Select POS", help='select POS for the user')
