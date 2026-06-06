# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SiteVisitSheet(models.Model):
    _name = 'cupama.site.visit.sheet'
    _description = 'Site Visit Sheet - SPC Flooring'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'date desc, id desc'

    # ── Identification ──────────────────────────────────────────
    name = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        default='New',
        copy=False,
        tracking=True,
    )
    date = fields.Date(
        string='Date',
        default=fields.Date.context_today,
        required=True,
        tracking=True,
    )
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order / Quotation',
        ondelete='cascade',
        index=True,
        tracking=True,
    )
    client_id = fields.Many2one(
        'res.partner',
        string='Client',
        related='sale_order_id.partner_id',
        store=True,
        readonly=True,
    )
    client_name = fields.Char(string='Name', tracking=True)
    tel_no = fields.Char(string='Tel No')
    address = fields.Text(string='Address')
    technician_name = fields.Char(string='Technician Name', tracking=True)
    expected_installation_date = fields.Date(
        string='Expected Installation Date',
        tracking=True,
    )

    # ── Measurements / Accessories ───────────────────────────────
    skirting = fields.Boolean(string='Skirting')
    bar_t_reducer = fields.Boolean(string='Bar T Reducer')

    # ── Floor Level ──────────────────────────────────────────────
    floor_level = fields.Selection(
        selection=[
            ('ground', 'Ground'),
            ('1', '1st Floor'),
            ('2', '2nd Floor'),
            ('3', '3rd Floor'),
        ],
        string='Floor Level',
        tracking=True,
    )

    # ══════════════════════════════════════════════════════════════
    # House Status Checklist
    # Chaque option (a→e) est évaluée séparément pour :
    #   - NEW property
    #   - RENOVATION property
    # ══════════════════════════════════════════════════════════════

    # a. Ease of Access
    ease_of_access_new = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Ease of Access (New)',
    )
    ease_of_access_renovation = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Ease of Access (Renovation)',
    )

    # b. Moveable and heavy items
    moveable_heavy_items_new = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Moveable & Heavy Items (New)',
    )
    moveable_heavy_items_renovation = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Moveable & Heavy Items (Renovation)',
    )

    # c. Electrical point
    electrical_point_new = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Electrical Point (New)',
    )
    electrical_point_renovation = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Electrical Point (Renovation)',
    )

    # d. Delivery possible
    delivery_possible_new = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Delivery Possible (New)',
    )
    delivery_possible_renovation = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Delivery Possible (Renovation)',
    )

    # e. Removal of flooring/skirting
    removal_flooring_skirting_new = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Removal of Flooring/Skirting (New)',
    )
    removal_flooring_skirting_renovation = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Removal of Flooring/Skirting (Renovation)',
    )

    # ── Flooring Surface Status ──────────────────────────────────
    flooring_surface_status = fields.Selection(
        selection=[
            ('tiles', 'Tiles'),
            ('incomplete', 'Incomplete'),
            ('polished', 'Polished'),
        ],
        string='Flooring Surface Status',
    )

    # ── Site Photos ──────────────────────────────────────────────
    photos_taken = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Photos Taken of Actual Areas',
    )
    photo_ids = fields.Many2many(
        'ir.attachment',
        'site_visit_photo_rel',
        'visit_id',
        'attachment_id',
        string='Site Photos',
    )

    # ── Client Instructions ──────────────────────────────────────
    client_informed = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Client Informed to Clear Areas',
    )

    # ── Additional Remarks ───────────────────────────────────────
    additional_remarks = fields.Text(string='Additional Remarks')

    # ── Dimensions (office use) ──────────────────────────────────
    dimension_ids = fields.One2many(
        'cupama.site.visit.dimension',
        'visit_id',
        string='Dimensions',
    )
    total_area = fields.Float(
        string='Total Area (m²)',
        compute='_compute_total_area',
        store=True,
    )

    # ── Conditions / Signature ───────────────────────────────────
    client_signature = fields.Binary(string='Client Signature', attachment=True)
    client_signature_name = fields.Char(default='signature.png')
    conditions_agreed = fields.Boolean(
        string='Conditions Agreed by Client',
        tracking=True,
    )

    # ── State ────────────────────────────────────────────────────
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        tracking=True,
        copy=False,
    )

    # ── Compute ──────────────────────────────────────────────────
    @api.depends('dimension_ids.area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = sum(rec.dimension_ids.mapped('area'))

    # ── Sequence ─────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'cupama.site.visit.sheet'
                ) or 'New'
        return super().create(vals_list)

    # ── Actions ──────────────────────────────────────────────────
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})


class SiteVisitDimension(models.Model):
    _name = 'cupama.site.visit.dimension'
    _description = 'Site Visit Dimension Line'

    visit_id = fields.Many2one(
        'cupama.site.visit.sheet',
        string='Visit Sheet',
        ondelete='cascade',
        required=True,
    )
    room_name = fields.Char(string='Room / Area', required=True)
    length = fields.Float(string='Length (m)', digits=(10, 2))
    width = fields.Float(string='Width (m)', digits=(10, 2))
    area = fields.Float(
        string='Area (m²)',
        compute='_compute_area',
        store=True,
        digits=(10, 2),
    )
    notes = fields.Char(string='Notes')

    @api.depends('length', 'width')
    def _compute_area(self):
        for rec in self:
            rec.area = rec.length * rec.width
