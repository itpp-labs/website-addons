# -*- coding: utf-8 -*-
from openerp.osv import osv, orm
from openerp.osv import fields as fields
from openerp import models
from openerp import fields as fields_new_api
class sale_order(osv.Model):
    _inherit = "sale.order"
    _columns = {
        'buy_way': fields.char(),
    }


class website_config_settings(models.TransientModel):
    _inherit = 'website.config.settings'
    module_nobill_noship = fields_new_api.Boolean("Pickup and pay at store")
    module_bill_noship = fields_new_api.Boolean("Pickup at store but pay now")
