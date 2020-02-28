# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    hide_add_to_cart_url = fields.Char("Add to Cart redirect link")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1,
        pricelist=False,
        parent_combination=False,
        only_template=False,
    ):
        res = super(ProductTemplate, self)._get_combination_info(
            combination,
            product_id,
            add_qty,
            pricelist,
            parent_combination,
            only_template,
        )
        res["price_with_taxes"] = (
            self.env["product.product"].browse(res["product_id"]).price
        )
        return res
