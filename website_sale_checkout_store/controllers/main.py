# -*- coding: utf-8 -*-
import werkzeug
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website_sale.controllers.main import website_sale

class website_sale(website_sale):
    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        cr, uid, context = request.cr, request.uid, request.context

        order = request.website.sale_get_order(force_create=1, context=context)

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection
        try:
            order.buy_way = post['buyMethod']
        except:
            pass
        if 'noship' in order.buy_way:
            website_sale.mandatory_billing_fields = ["name", "phone", "email"]
            website_sale.mandatory_shipping_fields = ["name", "phone", "email"]
        else:
            website_sale.mandatory_billing_fields = ["name", "phone", "email", "street2", "city", "country_id"]
            website_sale.mandatory_shipping_fields = ["name", "phone", "street", "city", "country_id"]
        values = self.checkout_values()
        values['order'] = order

        return request.website.render("website_sale.checkout", values)

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        cr, uid, context = request.cr, request.uid, request.context
        order = request.website.sale_get_order(context=context)
        if 'nobill' in order.buy_way:
            request.website.sale_reset(context=context)
            return request.redirect('/shop/confirmation')
        else:
            return super(website_sale, self).payment()
