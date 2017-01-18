# -*- coding: utf-8 -*-
from odoo import fields
from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_on_website = fields.Boolean('Show Add To Cart button', help='Switch off to disable sales via eCommerce', default=True)
