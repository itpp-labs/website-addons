# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteMultiCompanySale(WebsiteSale):
    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        response = super(WebsiteMultiCompanySale, self).shop(page=page, category=category, search=search, ppg=ppg, **post)
        categs = request.env['product.public.category'].search([
            ('parent_id', '=', False),
            '|',
            ('website_ids', '=', False),
            ('website_ids', 'in', [request.website.id]),
        ])
        response.qcontext.update({
            'categories': categs,
        })
        return response
