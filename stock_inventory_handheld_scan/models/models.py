# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, api, fields


class Inventory(models.Model):
    _inherit = "stock.inventory"

    @api.multi
    def action_check_barcode(self, barcode):
        for line in self.line_ids:
            product = line.product_id
            barcodes = line.product_id.multi_barcode_ids and line.product_id.multi_barcode_ids.mapped('barcode')
            if (product.barcode and product.barcode == barcode) or (barcodes and barcode in barcodes):
                return {
                    'line_id': line.id,
                    'product_id': product.id,
                    'product_name': product.product_tmpl_id.name,
                    'default_code': product.default_code,
                    'product_size': product.product_size,
                    'product_qty': line.product_qty,
                    'theoretical_qty': line.theoretical_qty,
                    'product_attributes': product.attribute_value_ids.mapped('name')
                }
        products = self.env['product.product'].search([('barcode', '=', barcode)])
        if products:
            return {
                'product_id': products[0].id,
                'product_name': products[0].product_tmpl_id.name,
            }
        partner_barcodes = self.env['res.partner.product.barcode'].search([('barcode', '=', barcode)])
        if partner_barcodes:
            return {
                'product_id': partner_barcodes[0].product_id.id,
                'product_name': partner_barcodes[0].product_id.product_tmpl_id.name,
            }
        return False


class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    @api.multi
    def action_update_inventory_line_qty(self, qty):
        self.write({
            'product_qty': qty,
        })


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_size = fields.Char('Product Size')
