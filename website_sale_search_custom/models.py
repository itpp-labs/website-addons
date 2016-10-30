# -*- coding: utf-8 -*-
from odoo import http, models, api
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale as controller


class WebsiteSale(controller):

    @http.route(['/shop',
                 '/shop/page/<int:page>',
                 '/shop/category/<model("product.public.category"):category>',
                 '/shop/category/<model("product.public.category"):category>/page/<int:page>'
                 ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', **post):
        new_context = request.context.copy()
        new_context['search_tags'] = search
        request.context = new_context
        if category and search:
            category = None
        return super(WebsiteSale, self).shop(page, category, search, **post)


class Product(models.Model):
    _inherit = 'product.template'

    def _extend_domain(self, domain):
        print '_extend_domain', self.env.context
        if not (self.env.context.get('search_tags')):
            return domain
        domain = ['|', ('tag_ids', 'ilike', self.env.context.get('search_tags'))] + domain
        return domain

    @api.model
    def search_count(self, domain):
        domain = self._extend_domain(domain)
        return super(Product, self).search_count(domain)

    @api.model
    def search(self, domain, offset=0, limit=None, order=None, count=False):
        domain = self._extend_domain(domain)
        return super(Product, self).search(domain, offset=offset, limit=limit, order=order, count=count)
