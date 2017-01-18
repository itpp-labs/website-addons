# -*- coding: utf-8 -*-
from odoo import fields
from odoo import models


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template', 'website_seo_url']

    seo_url = fields.Char('SEO URL', translate=True, index=True)
