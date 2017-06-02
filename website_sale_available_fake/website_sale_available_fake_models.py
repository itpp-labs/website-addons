# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp import fields
from openerp import models
import openerp.addons.decimal_precision as dp
from openerp.osv import osv, fields as old_fields
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class Website(osv.Model):
    _inherit = 'website'

    def sale_get_order(self, cr, uid, ids, force_create=False, code=None, update_pricelist=None, context=None):
        context = (context or {}).copy()
        context['product_available_fake'] = 1
        return super(Website, self).sale_get_order(cr, uid, ids, force_create, code, update_pricelist, context)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    limit_per_order = fields.Integer('Limit per order', default=0)
    private_sale = fields.Boolean('Private Sale', default=False, help='Sale only to selected Partners')
    private_sale_partner_ids = fields.Many2many('res.partner', 'product_private_sale_partner_rel', 'template_id',
                                                'partner_id', string='Private Sale Partners')
    qty_sale_recently = fields.Float(compute='_compute_qty_sale_recently', default=0)

    def _compute_qty_sale_recently(self):
        order_obj = self.env['sale.order']

        recent_order_date = datetime.now() - relativedelta(days=1)
        domain = [('state', '!=', 'cancel'), ('date_order', '>', recent_order_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT))]
        if self.env.context.get('order_id', False):
            domain.append(('id', '!=', self.env.context['order_id']))
        if self.env.context.get('partner_id', False):
            domain.append(('partner_id', '=', self.env.context['partner_id']))

        orders = order_obj.search(domain)

        for record in self:
            record.qty_sale_recently = 0
            product_ids = [p.id for p in record.product_variant_ids]

        for order in orders:
            for line in order.order_line:
                if line.product_id.id in product_ids:
                    line.product_id.product_tmpl_id.qty_sale_recently += line.product_uom_qty

    def _product_available(self, cr, uid, ids, field_names=None, arg=False, context=None):
        context = context or {}
        res = super(ProductTemplate, self)._product_available(cr, uid, ids, field_names, arg, context)

        if context.get('product_available_fake', False):
            product_obj = self.pool.get('product.template')
            product_limits = product_obj.read(cr, uid, res.keys(), ['limit_per_order'], context=context)
            product_limits = dict((p['id'], p['limit_per_order']) for p in product_limits)

            for id, product in res.iteritems():
                limit = product_limits.get(id, 0)
                if limit > 0 and limit < product['qty_available']:
                    res[id]['qty_available'] = limit
                if limit > 0 and limit < product['virtual_available']:
                    res[id]['virtual_available'] = limit
        return res

    def _search_product_quantity(self, cr, uid, obj, name, domain, context):
        return super(ProductTemplate, self)._search_product_quantity(cr, uid, obj, name, domain, context)

    _columns = {
        'virtual_available': old_fields.function(_product_available, multi='qty_available',
                                                 type='float', digits_compute=dp.get_precision('Product Unit of Measure'),
                                                 fnct_search=_search_product_quantity, string='Quantity Available'),
    }


class ResPartner(models.Model):
    _inherit = 'res.partner'

    private_sale_product_ids = fields.Many2many('product.template', 'product_private_sale_partner_rel', 'partner_id',
                                                'template_id', string='Private Sale Products')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _product_available(self, cr, uid, ids, field_names=None, arg=False, context=None):
        context = context or {}
        res = super(ProductProduct, self)._product_available(cr, uid, ids, field_names, arg, context)

        if context.get('product_available_fake', False):
            product_obj = self.pool.get('product.product')
            product_limits = product_obj.read(cr, uid, res.keys(), ['limit_per_order'], context=context)
            product_limits = dict((p['id'], p['limit_per_order']) for p in product_limits)

            for id, product in res.iteritems():
                limit = product_limits.get(id, 0)
                if limit > 0 and limit < product['qty_available']:
                    res[id]['qty_available'] = limit
                if limit > 0 and limit < product['virtual_available']:
                    res[id]['virtual_available'] = limit
        return res

    def _search_product_quantity(self, cr, uid, obj, name, domain, context):
        return super(ProductProduct, self)._search_product_quantity(cr, uid, obj, name, domain, context)

    _columns = {
        'virtual_available': old_fields.function(_product_available, multi='qty_available',
                                                 type='float', digits_compute=dp.get_precision('Product Unit of Measure'),
                                                 fnct_search=_search_product_quantity, string='Quantity Available'),
    }


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def check_cheat_on_limited_products(self):
        for l in self.order_line:
            if l.product_id.limit_per_order:
                qty_sale_recently = l.product_id.product_tmpl_id.with_context({
                    'partner_id': self.partner_id.id,
                    'order_id': self.id
                }).qty_sale_recently
                if l.product_uom_qty + qty_sale_recently > l.product_id.limit_per_order:
                    available_qty = l.product_id.limit_per_order - qty_sale_recently
                    if available_qty > 0:
                        # decrease quantity of product
                        self.write({'order_line': [(1, l.id, {'product_uom_qty': available_qty})]})
                    else:
                        # limit exceed, remove line
                        self.write({'order_line': [(2, l.id)]})
        return True
