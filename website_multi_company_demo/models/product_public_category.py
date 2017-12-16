# -*- coding: utf-8 -*-
from odoo import models


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    def init(self):
        """Set default website for all categories without website value"""
        IS_INITED = 'product_public_category_is_inited'

        if self.env['ir.config_parameter'].get_param(IS_INITED):
            return

        self.search([('website_ids', '=', False)]).write({
            'website_ids': [
                (4, self.env.ref('website.default_website').id, 0)
            ]})

        self.env['ir.config_parameter'].set_param(IS_INITED, '1')
