# -*- coding: utf-8 -*-
from openerp import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"
    buy_now = fields.Boolean('Is Buy now')
