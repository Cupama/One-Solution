# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    site_visit_count = fields.Integer(
        string='Site Visits',
        compute='_compute_site_visit_count',
    )

    def _compute_site_visit_count(self):
        SiteVisit = self.env['cupama.site.visit.sheet']
        for order in self:
            order.site_visit_count = SiteVisit.search_count(
                [('sale_order_id', '=', order.id)]
            )

    def action_view_site_visits(self):
        self.ensure_one()
        visits = self.env['cupama.site.visit.sheet'].search(
            [('sale_order_id', '=', self.id)]
        )
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Site Visit Sheets',
            'res_model': 'cupama.site.visit.sheet',
            'view_mode': 'list,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {
                'default_sale_order_id': self.id,
                'default_client_name': self.partner_id.name,
                'default_address': self.partner_id._display_address(),
                'default_tel_no': self.partner_id.phone,
            },
        }
        if len(visits) == 1:
            action['view_mode'] = 'form'
            action['res_id'] = visits.id
        return action

    def action_create_site_visit(self):
        self.ensure_one()
        visit = self.env['cupama.site.visit.sheet'].create({
            'sale_order_id': self.id,
            'client_name': self.partner_id.name,
            'address': self.partner_id._display_address(),
            'tel_no': self.partner_id.phone or '',
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Site Visit Sheet',
            'res_model': 'cupama.site.visit.sheet',
            'view_mode': 'form',
            'res_id': visit.id,
        }
