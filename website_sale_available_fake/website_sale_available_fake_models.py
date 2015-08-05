from openerp import api, models, fields
import openerp.addons.decimal_precision as dp
from openerp.osv import osv, fields as old_fields


class product_template(models.Model):
    _inherit = 'product.template'

    limit_per_order = fields.Integer('Limit per order', default=0)
    private_sale = fields.Boolean('Private Sale', default=False)
    private_sale_partner_ids = fields.Many2many('res.partner', 'product_private_sale_partner_rel', 'template_id', 
        'partner_id', string='Private Sale Partners')

    def _product_available(self, cr, uid, ids, field_names=None, arg=False, context=None):
        context = context or {}
        product_obj = self.pool.get('product.template')

        res = super(product_template, self)._product_available(cr, uid, ids, field_names, arg, context)

        product_limits = product_obj.read(cr, uid, res.keys(), ['limit_per_order'], context=context)
        product_limits = dict((p['id'], p['limit_per_order']) for p in product_limits)

        if context.get('product_available_fake', False):
            for id, product in res.iteritems():
                limit = product_limits.get(id, 0)
                if limit > 0 and limit < product['qty_available']:
                    res[id]['qty_available'] = limit
                if limit > 0 and limit < product['virtual_available']:
                    res[id]['virtual_available'] = limit
        return res

    def _search_product_quantity(self, cr, uid, obj, name, domain, context):
        return super(product_template, self)._search_product_quantity(cr, uid, obj, name, domain, context)

    _columns = {
        'qty_available': old_fields.function(_product_available, multi='qty_available',
            type='float', digits_compute=dp.get_precision('Product Unit of Measure'),
            fnct_search=_search_product_quantity, string='Quantity On Hand'),
    }


class res_partner(models.Model):
    _inherit = 'res.partner'

    private_sale_product_ids = fields.Many2many('product.template', 'product_private_sale_partner_rel', 'partner_id', 
        'template_id', string='Private Sale Products')


class product_product(models.Model):
    _inherit = 'product.product'

    def _product_available(self, cr, uid, ids, field_names=None, arg=False, context=None):
        context = context or {}
        product_obj = self.pool.get('product.product')

        res = super(product_product, self)._product_available(cr, uid, ids, field_names, arg, context)

        product_limits = product_obj.read(cr, uid, res.keys(), ['limit_per_order'], context=context)
        product_limits = dict((p['id'], p['limit_per_order']) for p in product_limits)

        if context.get('product_available_fake', False):
            for id, product in res.iteritems():
                limit = product_limits.get(id, 0)
                if limit > 0 and limit < product['qty_available']:
                    res[id]['qty_available'] = limit
                if limit > 0 and limit < product['virtual_available']:
                    res[id]['virtual_available'] = limit
        return res

    def _search_product_quantity(self, cr, uid, obj, name, domain, context):
        return super(product_product, self)._search_product_quantity(cr, uid, obj, name, domain, context)

    _columns = {
        'qty_available': old_fields.function(_product_available, multi='qty_available',
            type='float', digits_compute=dp.get_precision('Product Unit of Measure'),
            fnct_search=_search_product_quantity, string='Quantity On Hand'),
    }


class sale_order(models.Model):
    _inherit = 'sale.order'

    def check_cheat_on_limited_products(self):
        product_ids = [l.product_id.id for l in self.order_line]
        # select limited product quantities for last 24  hours for the customer
        self.env.cr.execute("""SELECT p.id, SUM(l.product_uom_qty) as qty, t.limit_per_order 
                            FROM product_product p 
                            INNER JOIN product_template t ON p.product_tmpl_id = t.id 
                            LEFT JOIN sale_order_line l ON l.product_id = p.id AND l.order_id != %(order_id)s
                            LEFT JOIN sale_order o ON l.order_id = o.id  
                            AND o.partner_id = %(partner_id)s AND o.date_confirm > (NOW() - '1 day'::INTERVAL)
                            WHERE p.id IN %(product_ids)s 
                            AND t.limit_per_order > 0 
                            GROUP BY p.id, t.id""",
                            {'partner_id': self.partner_id.id, 'product_ids': tuple(product_ids), 'order_id': self.id})
        product_info = dict([(p[0], p) for p in self.env.cr.fetchall()])

        for l in self.order_line:
            product = product_info.get(l.product_id.id, False)
            if product:
                if l.product_uom_qty + product[1] > product[2]:
                    available_qty = product[2] - product[1]
                    if available_qty > 0:
                        # decrease quantity of product
                        self.write({'order_line': [(1, l.id, {'product_uom_qty': available_qty})]})
                    else:
                        # limit exceed, remove line
                        self.write({'order_line': [(2, l.id)]})
        return True
