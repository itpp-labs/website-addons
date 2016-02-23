from openerp.osv import osv, orm, fields

class sale_order(osv.Model):
    _inherit = "sale.order"

    def _cart_update(self, cr, uid, ids, product_id=None, line_id=None, add_qty=0, set_qty=0, context=None, **kwargs):
        product = self.pool['product.product'].browse(cr, uid, product_id)
        if product.sale_one_only:
            add_qty = 0
            set_qty = 1
        return super(sale_order, self)._cart_update(cr, uid, ids, product_id, line_id, add_qty, set_qty, context=context, **kwargs)
