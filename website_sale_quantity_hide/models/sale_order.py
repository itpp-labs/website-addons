# -*- coding: utf-8 -*-
from openerp import models, http


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0):
        product = http.request.env['product.product'].browse(product_id)
        if product.sale_one_only:
            add_qty = 0
            set_qty = 1
        return super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty)
