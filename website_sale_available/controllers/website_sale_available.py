# -*- coding: utf-8 -*-
import logging

from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class Controller(WebsiteSale):

    def checkout_redirection(self, order):
        res = super(Controller, self).checkout_redirection(order=order)
        order = request.website.sale_get_order(context=request.context)

        if not all([
                line.product_uom_qty <= line.product_id.virtual_available
                for line in order.order_line if not line.is_delivery
        ]):
            return request.redirect("/shop/cart")

        return res
