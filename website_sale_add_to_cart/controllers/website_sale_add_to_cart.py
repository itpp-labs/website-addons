from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class PosWebsiteSale(http.Controller):
    @http.route(["/shop/get_order_numbers"], type="json", auth="public", website=True)
    def get_order_numbers(self):
        res = {}
        order = request.website.sale_get_order()
        if order:
            for line in order.website_order_line:
                res[line.product_id.id] = line.product_uom_qty
        return res


class WebsiteSaleExtended(WebsiteSale):
    @http.route()
    def get_unit_price(self, product_ids, add_qty, **post):
        products = (
            request.env["product.product"]
            .with_context({"quantity": add_qty})
            .browse(product_ids)
        )
        if add_qty == 0:
            return {product.id: 0 for product in products}
        return super(WebsiteSaleExtended, self).get_unit_price(
            product_ids, add_qty, **post
        )
