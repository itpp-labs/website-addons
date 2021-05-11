from odoo import http
from odoo.http import request

from odoo.addons.web.controllers.main import ensure_db
from odoo.addons.website.controllers.main import Home


class Home(Home):
    @http.route()
    def web_login(self, redirect=None, *args, **kw):
        ensure_db()
        response = super(Home, self).web_login(redirect=redirect, *args, **kw)
        init_page = kw.get("init_page")
        response.qcontext.update({"init_page": init_page})

        if not redirect and request.params["login_success"]:
            if (
                request.env["res.users"]
                .browse(request.uid)
                .has_group("base.group_user")
            ):
                redirect = b"/web?" + request.httprequest.query_string
            else:
                init_page = request.params.get("init_page")
                if init_page:
                    redirect = init_page
                else:
                    redirect = "/my"
            return http.redirect_with_hash(redirect)
        return response
