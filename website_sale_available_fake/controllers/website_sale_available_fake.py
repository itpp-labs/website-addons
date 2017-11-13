# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class controller(WebsiteSale):

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        request.context.update({'product_available_fake': 1})
        r = super(Controller, self).product(product, category, search, **kwargs)
        return r

    @http.route(['/shop/confirm_order'], type='http', auth="public", website=True)
    def confirm_order(self, **post):
        order = request.website.sale_get_order(context=request.context)
        order.check_cheat_on_limited_products()
        r = super(Controller, self).confirm_order(**post)
        return r

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, **post):
        request.context.update({'product_available_fake': 1})
        r = super(Controller, self).cart(**post)
        return r
