# -*- coding: utf-8 -*-
from odoo import _, models
from odoo.exceptions import UserError


class CupamaDeleteGuardMixin(models.AbstractModel):
    """Refuse deletion for users outside the dedicated group (#9).

    Applied to the main business documents below. System operations
    (``sudo``/superuser) keep working so automated flows are not broken.
    """
    _name = 'cupama.delete.guard.mixin'
    _description = 'Deletion restricted to administrators'

    def unlink(self):
        if (
            self
            and not self.env.su
            and not self.env.user.has_group('cupama_security.group_can_delete')
        ):
            raise UserError(_(
                "Deleting %(document)s records is reserved to administrators.\n"
                "Archive the record instead, or ask an administrator.",
                document=self.env['ir.model']._get(self._name).name,
            ))
        return super().unlink()


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'cupama.delete.guard.mixin']


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template', 'cupama.delete.guard.mixin']


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'cupama.delete.guard.mixin']


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'cupama.delete.guard.mixin']


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order', 'cupama.delete.guard.mixin']


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'cupama.delete.guard.mixin']


class AccountPayment(models.Model):
    _name = 'account.payment'
    _inherit = ['account.payment', 'cupama.delete.guard.mixin']


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'cupama.delete.guard.mixin']
