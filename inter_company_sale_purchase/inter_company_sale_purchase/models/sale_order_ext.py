from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class SaleOrderExt(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        record = super(SaleOrderExt, self).create(vals)

        parent_company = self.env['res.company'].browse(1)
        child_company = self.env['res.company'].browse(2)
        if self.env.company.id == 1 and record.partner_id.id == 22:
            record.action_confirm()
            # Prepare PO values
            po_vals = {
                'partner_id': parent_company.partner_id.id,
                'company_id': child_company.id,
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
            # Create the PO
            purchase_order = self.env['purchase.order'].sudo().create(po_vals)
            purchase_order.button_confirm()

        return record










        # # Get the company of the SO partner
        # partner_company = self.partner_id.parent_id
        # if partner_company.name == 'Babo Cupama Household Co Ltd':
        #     # Assuming you have a company relation or some logic to identify the correct company
        #     company_id = self.env['res.company'].search([('name', '=', 'CUPAMA LTD')], limit=1)
        #     if company_id:
        #         # Prepare PO values
        #         po_vals = {
        #             'partner_id': company_id.partner_id.id,
        #             'company_id': partner_company.id,
        #             'date_order': fields.Date.today(),
        #             'order_line': [(0, 0, {
        #                 'name': line.product_id.name,
        #                 'product_id': line.product_id.id,
        #                 'product_qty': line.product_uom_qty,
        #                 'product_uom': line.product_uom.id,
        #                 'price_unit': line.price_unit,
        #                 'date_planned': fields.Date.today(),
        #             }) for line in self.order_line],
        #         }
        #         # Create the PO
        #         self.env['purchase.order'].sudo().create(po_vals)