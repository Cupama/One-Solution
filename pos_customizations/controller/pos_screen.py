# -*- coding: utf-8 -*-
from odoo.http import request
from odoo.addons.web.controllers.home import Home


class PosLoginRedirect(Home):
    """Send POS-only users straight to their configured Point of Sale after login.

    Users that belong to ``group_allow_backend`` keep the standard backend
    redirection. Everyone else who has a POS configured (``pos_conf_id``) is
    redirected to ``/pos/ui/<config_id>``, which opens (creating it if needed)
    the matching POS session.
    """

    def _login_redirect(self, uid, redirect=None):
        url = super()._login_redirect(uid, redirect=redirect)
        user = request.env['res.users'].sudo().browse(uid)
        if not user.has_group('pos_customizations.group_allow_backend') and user.pos_conf_id:
            return '/pos/ui/%d' % user.pos_conf_id.id
        return url
