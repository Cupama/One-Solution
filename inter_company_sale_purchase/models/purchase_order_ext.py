from odoo import api, fields, models

class PurchaseOrderExt(models.Model):
    _inherit = 'purchase.order'

    sale_order = fields.Char(string='Sale Order')
