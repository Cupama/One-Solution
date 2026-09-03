# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # New shops are restricted by default too (#10).
    restrict_price_control = fields.Boolean(default=True)
