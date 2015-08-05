# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale


class controller(website_sale):

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        request.context.update({'product_available_fake': 1})
        r = super(controller, self).product(product, category, search, **kwargs)
        return r

    @http.route(['/shop/confirm_order'], type='http', auth="public", website=True)
    def confirm_order(self, **post):
        order = request.website.sale_get_order(context=request.context)
        order.check_cheat_on_limited_products()
        r = super(controller, self).confirm_order(**post)
        return r
