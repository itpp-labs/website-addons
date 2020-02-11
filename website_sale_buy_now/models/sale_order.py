# -*- coding: utf-8 -*-
from openerp import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    buy_now = fields.Boolean("Is Buy now")
