# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _cart_update(
        self,
        product_id=None,
        line_id=None,
        add_qty=0,
        set_qty=0,
        attributes=None,
        **kwargs
    ):
        order_lines = False
        if line_id is not False:
            order_lines = self._cart_find_product_line(product_id, line_id, **kwargs)
            order_line = order_lines and order_lines[0]

        if order_line and order_line.event_id and "registration_data" not in kwargs:
            # _cart_update can be called in registration_confirm and registration_data is a way to exclude that case
            quantity = 0
            # compute new quantity
            if set_qty:
                quantity = set_qty
            elif add_qty is not None:
                quantity = order_line.product_uom_qty + (add_qty or 0)

            if quantity != 0:
                # don't allow to change Event product
                return {
                    "line_id": order_line.id,
                    "quantity": order_line.product_uom_qty,
                }

        return super(SaleOrder, self)._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            attributes=attributes,
            **kwargs
        )
