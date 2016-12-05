# -*- coding: utf-8 -*-
from openerp import http
from openerp.addons.website_sale.controllers.main import website_sale as controller


class WebsiteSale(controller):

    @http.route()
    def shop(self, page=0, category=None, search='', **post):
        if category and search:
            category = None
        return super(WebsiteSale, self).shop(page, category, search, **post)
