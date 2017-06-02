# -*- coding: utf-8 -*-
from openerp import fields
from openerp import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_on_website = fields.Boolean('Show Add To Cart button', help='Switch off to disable sales via eCommerce', default=True)
