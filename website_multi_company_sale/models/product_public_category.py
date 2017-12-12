# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    website_ids = fields.Many2many(
        'website',
        string="Websites",
        help="On which websites show category. Keep empty to show at all websites. The value is ignored if there is Parent Category"
    )
