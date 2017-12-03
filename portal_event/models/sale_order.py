# -*- coding: utf-8 -*-
from odoo import models, api, fields
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = 'sale.order'

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

