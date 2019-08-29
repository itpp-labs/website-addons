from odoo import models, api, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def add_refund_line(self, refund_source_line, name, qty=0):
        self.ensure_one()
        if 0 < qty < refund_source_line.product_uom_qty:
            refund_price = refund_source_line.price_unit * qty
        else:
            refund_price = refund_source_line.price_total
        # TODO make product customizable
        refund_product = self.env.ref('website_sale_refund.refund_product')
        product_id = refund_product.id
        SaleOrderLineSudo = self.env['sale.order.line'].sudo()
        order_line = SaleOrderLineSudo.search([
            ('order_id', '=', self.id),
            ('product_id', '=', product_id),
            ('refund_source_line_id', '=', refund_source_line.id),
        ], limit=1)
        if order_line:
            return order_line
        values = self._website_product_id_change(self.id, product_id, qty=1)
        values['name'] = name
        values['price_unit'] = -1 * refund_price
        values['tax_id'] = False
        values['refund_source_line_id'] = refund_source_line.id
        order_line = SaleOrderLineSudo.create(values)
        return order_line

    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, attributes=None, **kwargs):
        order_lines = False
        if line_id is not False:
            order_lines = self._cart_find_product_line(product_id, line_id, **kwargs)
            order_line = order_lines and order_lines[0]

        if order_line and order_line.price_unit < 0:
            quantity = 0
            # compute new quantity
            if set_qty:
                quantity = set_qty
            elif add_qty is not None:
                quantity = order_line.product_uom_qty + (add_qty or 0)

            if quantity != 0:
                # don't allow to change refund product
                return {'line_id': order_line.id, 'quantity': order_line.product_uom_qty}

        return super(SaleOrder, self)._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, attributes=attributes, **kwargs)

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        res = super(SaleOrder, self).action_confirm()
        refunded_lines = self.order_line.mapped('refund_source_line_id')
        refunded_lines._cancel_line(origin=self)
        return res


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    refund_source_line_id = fields.Many2one('sale.order.line', 'Refund Source Line', help='Order line that is used for refund')

    @api.multi
    def _cancel_line(self, origin=None):
        # Origin - sale order, that cancels this line
        # TODO: cancel delivery, etc
        return True
