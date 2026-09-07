# -*- coding: utf-8 -*-
import re

from werkzeug import urls

from odoo import _, models
from odoo.exceptions import UserError

DEFAULT_PHONE_CODE = '230'  # Mauritius


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_whatsapp_target(self):
        """International number for wa.me, digits only (e.g. 23058207534)."""
        self.ensure_one()
        # 'mobile' no longer exists on recent Odoo 19 revisions: only use
        # the candidate fields the model actually carries.
        raw = ''
        for fname in ('whatsapp_number', 'mobile', 'phone'):
            if fname in self._fields and self[fname]:
                raw = self[fname]
                break
        digits = re.sub(r'\D', '', raw)
        if not digits:
            return False
        if raw.strip().startswith('+') or digits.startswith('00'):
            return digits.lstrip('0') if digits.startswith('00') else digits
        code = str(self.country_id.phone_code or DEFAULT_PHONE_CODE)
        if digits.startswith(code) and len(digits) > 8:
            return digits
        return code + digits.lstrip('0')

    def _whatsapp_action(self, message=''):
        self.ensure_one()
        number = self._get_whatsapp_target()
        if not number:
            raise UserError(_(
                "No WhatsApp number, mobile or phone on %s.\n"
                "Fill the WhatsApp Number field on the contact first.",
                self.display_name,
            ))
        url = 'https://wa.me/%s' % number
        if message:
            url += '?text=%s' % urls.url_quote(message)
        return {'type': 'ir.actions.act_url', 'url': url, 'target': 'new'}

    def action_open_whatsapp(self):
        return self._whatsapp_action()
