# Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, api, fields


class VendorBarcode(models.Model):

    _name = 'res.partner.product.barcode'
    _description = 'Vendor Product Multiple Barcodes'

    barcode = fields.Char('Barcode', required=True)
    partner_id = fields.Many2one('res.partner', 'Vendor', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    supplier_info_id = fields.Many2one('product.supplierinfo', 'Supplier Info')

    @api.model
    def create(self, vals):
        record = super(VendorBarcode, self).create(vals)
        if not vals.get('supplier_info_id', False):
            product_template_id = self.env['product.product'].browse(vals.get('product_id')).product_tmpl_id
            supplier_info_id = self.env['product.supplierinfo'].search([('name', '=', vals.get('partner_id')), '|', ('product_tmpl_id', '=', product_template_id.id), ('product_id', '=', vals.get('product_id'))])
            record.write({
                'supplier_info_id': supplier_info_id.id,
            })
        return record


class Partner(models.Model):

    _inherit = 'res.partner'

    multi_barcode_ids = fields.One2many('res.partner.product.barcode', 'partner_id', string='Product Barcodes')


class ProductProduct(models.Model):

    _inherit = 'product.product'

    multi_barcode_ids = fields.One2many('res.partner.product.barcode', 'product_id', string='Vendor Barcodes')


class SupplierInfo(models.Model):

    _inherit = "product.supplierinfo"

    multi_barcode_ids = fields.One2many('res.partner.product.barcode', 'supplier_info_id', string='Supplier Barcodes')


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def process_barcode_from_ui(self, barcode_str, visible_op_ids):
        """This function is called each time there barcode scanner reads an input"""
        self.ensure_one()
        pack_op = self.env['stock.move.line'].search(
            [('picking_id', '=', self.id)])
        matching_vendor_product_ids = self.env['res.partner.product.barcode'].search(
            [('barcode', '=', barcode_str)])
        answer = {'filter_loc': False, 'operation_id': False}
        if matching_vendor_product_ids:
            op_id = pack_op._increment(
                self.id,
                [('product_id', '=', matching_vendor_product_ids[0].product_id.id)],
                filter_visible=True,
                visible_op_ids=visible_op_ids,
                increment=True
            )
            answer['operation_id'] = op_id.id
            return answer
        return super(StockPicking, self).process_barcode_from_ui(barcode_str, visible_op_ids)
