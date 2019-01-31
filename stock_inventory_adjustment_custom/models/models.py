# Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, api, fields, _


class Inventory(models.Model):
    _inherit = "stock.inventory"

    supplier_id = fields.Many2one('product.supplierinfo', 'Supplier',
                                  readonly=True, states={'draft': [('readonly', False)]})
    negative_location = fields.Many2one(
        'stock.location', 'Inventoried Location',
        readonly=True, states={'draft': [('readonly', False)]})


    @api.model
    def _selection_filter(self):
        res_filter = super(Inventory, self)._selection_filter()
        res_filter.append(('supplier', _('Supplier')))
        res_filter.append(('negative_stock', _('Negative Stock')))
        return res_filter

    def _get_inventory_lines_values(self):

        vals = []
        quants = self.env['stock.quant']

        if self.filter == 'supplier':
            vendors = self.supplier_id.search([('name', '=', self.supplier_id.name.id)])
            vendors_prods = vendors.mapped('product_id')

            quants = quants.search([('product_id', 'in', vendors_prods.ids), ('quantity', '>=', 0)])

        if self.filter == 'negative_stock':

            quants = quants.search([('location_id', '=', self.negative_location.id)])

        if self.filter in ['supplier', 'negative_stock']:
            for q in quants:
                vals.append({
                    'location_id': q.location_id.id,
                    'package_id': q.package_id.id,
                    'partner_id': False,
                    'prod_lot_id': False,
                    'product_id': q.product_id.id,
                    'product_qty': q.quantity,
                    'product_uom_id': q.product_uom_id.id,
                    'theoretical_qty': q.quantity,
                })
            return vals

        return super(Inventory, self)._get_inventory_lines_values()
