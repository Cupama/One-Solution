# -*- coding: utf-8 -*-
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # -- #17 Additional delivery -------------------------------------------
    is_additional_delivery = fields.Boolean(
        string='Additional Delivery',
        copy=False,
        readonly=True,
        help="Delivery created afterwards from the sales order through the "
             "Additional Delivery action.",
    )
    additional_delivery_reason = fields.Char(
        string='Additional Delivery Reason',
        copy=False,
        readonly=True,
    )
