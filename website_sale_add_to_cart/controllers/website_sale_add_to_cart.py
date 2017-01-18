# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class PosWebsiteSale(http.Controller):

    @http.route(['/shop/get_order_numbers'], type='json', auth="public", website=True)
    def get_order_numbers(self):
        res = {}
        order = request.website.sale_get_order()
        if order:
            for line in order.website_order_line:
                res[line.product_id.id] = line.product_uom_qty
        return res
