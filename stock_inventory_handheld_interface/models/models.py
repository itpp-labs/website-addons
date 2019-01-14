# Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, api, fields


class Inventory(models.Model):
    _inherit = "stock.inventory"

    @api.multi
    def action_done_by_handheld(self, lines):
        for line in lines:
            self.line_ids.browse(line['res_id']).write({
                'product_qty': line['product_qty']
            })
        return True


class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    product_barcode = fields.Char('Product Barcode', related='product_id.barcode', store=True)
