from odoo import http
from odoo.http import request
import werkzeug
from odoo.addons.web.controllers.main import home


class PosScreen(home.Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        res = super().web_login(redirect=redirect, **kw)
        if request.env.user.has_group('pos_customizations.group_allow_backend'):
            return res
        else:
            pos_conf = request.env.user.pos_conf_id
            if pos_conf:
                if not pos_conf.current_session_id:
                    request.env['pos.session'].sudo().create({
                        'user_id': request.env.uid,
                        'config_id': pos_conf.id
                    })
                return werkzeug.utils.redirect('/pos/ui')
        return res