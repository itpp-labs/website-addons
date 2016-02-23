# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale as website_sale_controller


class website_sale(website_sale_controller):

    @http.route()
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        buy_now = kw.get('buy_now')
        if buy_now:
            order = request.website.sale_get_order()
            if order:
                for line in order.website_order_line:
                    line.unlink()
        res = super(website_sale, self).cart_update(product_id, add_qty, set_qty, **kw)
        if buy_now:
            order = request.website.sale_get_order()
            order.buy_now = True
            return request.redirect("/shop/checkout")

        return res
