# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request

from openerp.addons.website_sale.controllers.main import website_sale as controller


class WebsiteSale(controller):

    @http.route()
    def shop(self, page=0, category=None, search='', **post):
        request.context['search_tags'] = search
        return super(WebsiteSale, self).shop(page, category, search, **post)
