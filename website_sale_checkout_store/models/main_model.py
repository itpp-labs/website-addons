# -*- coding: utf-8 -*-
from openerp.osv import osv
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
    nobill_noship = fields_new_api.Boolean("Pickup and pay at store")
    bill_noship = fields_new_api.Boolean("Pickup at store but pay now")
    bill_ship = fields_new_api.Boolean("Pay now and get delivery")
    nobill_ship = fields_new_api.Boolean("Pay on delivery")
    default_option = fields_new_api.Selection([
        ('nobill_noship', 'Pickup and pay at store'),
        ('bill_noship', 'Pickup at store but pay now'),
        ('bill_ship', 'Pay now and get delivery'),
        ('nobill_ship', 'Pay on delivery'),
        ], string='Selected by default', default='nobill_noship')

    def set_nobill_noship(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "website_sale_checkout_store.nobill_noship", record.nobill_noship or '', context=context)

    def set_bill_noship(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "website_sale_checkout_store.bill_noship", record.bill_noship or '', context=context)

    def set_bill_ship(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "website_sale_checkout_store.bill_ship", record.bill_ship or '', context=context)

    def set_nobill_ship(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "website_sale_checkout_store.nobill_ship", record.nobill_ship or '', context=context)

    def set_default_option(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "website_sale_checkout_store.default_option", record.default_option or '', context=context)

    def get_default_nobill_noship(self, cr, uid, ids, context=None):
        nobill_noship = self.pool.get("ir.config_parameter").get_param(cr, uid, "website_sale_checkout_store.nobill_noship", default=False, context=context)
        return {'nobill_noship': nobill_noship}

    def get_default_bill_noship(self, cr, uid, ids, context=None):
        bill_noship = self.pool.get("ir.config_parameter").get_param(cr, uid, "website_sale_checkout_store.bill_noship", default=False, context=context)
        return {'bill_noship': bill_noship}

    def get_default_bill_ship(self, cr, uid, ids, context=None):
        bill_ship = self.pool.get("ir.config_parameter").get_param(cr, uid, "website_sale_checkout_store.bill_ship", default=False, context=context)
        return {'bill_ship': bill_ship}

    def get_default_nobill_ship(self, cr, uid, ids, context=None):
        nobill_ship = self.pool.get("ir.config_parameter").get_param(cr, uid, "website_sale_checkout_store.nobill_ship", default=False, context=context)
        return {'nobill_ship': nobill_ship}

    def get_default_default_option(self, cr, uid, ids, context=None):
        default_option = self.pool.get("ir.config_parameter").get_param(cr, uid, "website_sale_checkout_store.default_option", default='nobill_noship', context=context)
        return {'default_option': default_option}
