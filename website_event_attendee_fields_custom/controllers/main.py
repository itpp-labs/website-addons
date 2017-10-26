# -*- coding: utf-8 -*-

from odoo import http
from odoo.addons.website_event_sale.controllers.main import WebsiteEventController


class RequireLoginToRegister(WebsiteEventController):
    @http.route(auth="user")
    def event_register(self, event, **post):
        return super(RequireLoginToRegister, self).event_register(event, **post)
