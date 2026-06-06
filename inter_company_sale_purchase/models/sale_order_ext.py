from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrderExt(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        active_company = self.env.company
        parent_company = active_company
        child_companies = self.env['res.company'].search([]).filtered(
            lambda company: company.id != active_company.id
        )

        for record in records:
            for child in child_companies:
                if record.partner_id.id == child.partner_id.id:
                    if not record.order_line:
                        raise ValidationError(_("Please enter product in order lines."))
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
                            'product_uom_id': line.product_uom_id.id,
                            'price_unit': line.price_unit,
                            'date_planned': fields.Date.today(),
                        }) for line in record.order_line],
                    }
                    purchase_order = self.env['purchase.order'].sudo().create(po_vals)
                    purchase_order.button_confirm()

        return records
