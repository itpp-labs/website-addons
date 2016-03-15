# -*- coding: utf-8 -*-
from openerp.osv import osv, orm
from openerp.osv import fields as fields
from openerp import models
from openerp import fields as fields9
class sale_order(osv.Model):
    _inherit = "sale.order"
    _columns = {
        'buy_way': fields.char(),
    }


class website_config_settings(models.TransientModel):
    _inherit = 'website.config.settings'
    nobill_noship = fields9.Boolean("Pickup and pay at store")
    bill_noship = fields9.Boolean("Pickup at store but pay now")
