# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
import logging
import requests

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger("WooCommerce")


class ResPartner(models.Model):
    _inherit = "res.partner"

    brn_no = fields.Char('BRN')




class Res_company_inherit(models.Model):
        _inherit = 'res.company'

        brn_number = fields.Char('BRN NO')