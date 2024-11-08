from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class SaleOrderExt(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        record = super(SaleOrderExt, self).create(vals)

        active_company = self.env.company
        child_companies = []
        parent_company = None
        companies = self.env['res.company'].search([])
        for company in companies:
            if active_company.id == company.id:
                parent_company = company
            else:
                child_companies.append(company)
        for child in child_companies:
            if record.partner_id.id == child.partner_id.id:
                record.action_confirm()
                po_vals = {
                    'partner_id': parent_company.partner_id.id,
                    'company_id': child.id,
                    'payment_term_id': record.payment_term_id.id,
                    'date_order': fields.Date.today(),
                    'sale_order': record.name,
                    'order_line': [(0, 0, {
                        'name': line.product_id.name,
                        'product_id': line.product_id.id,
                        'product_qty': line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'price_unit': line.price_unit,
                        'date_planned': fields.Date.today(),
                    }) for line in record.order_line],
                }
            purchase_order = self.env['purchase.order'].sudo().create(po_vals)
            purchase_order.button_confirm()

        return record
