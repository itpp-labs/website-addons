# -*- coding: utf-8 -*-
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale


class WebsiteSale(website_sale):

    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        order = request.website.sale_get_order(force_create=1, context=request.context)

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection
        try:
            order.buy_way = post['buyMethod']
        except:
            pass
        values = self.checkout_values()
        values['order'] = order

        return request.website.render("website_sale.checkout", values)

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        context = request.context
        order = request.website.sale_get_order(context=context)
        if 'nobill' in order.buy_way:
            order.force_quotation_send()
            request.website.sale_reset(context=context)
            return request.redirect('/shop/confirmation')
        else:
            return super(WebsiteSale, self).payment()

    @http.route('/shop/payment/get_status/<int:sale_order_id>', type='json', auth="public", website=True)
    def payment_get_status(self, sale_order_id, **post):
        cr, context = request.cr, request.context

        order = request.registry['sale.order'].browse(cr, SUPERUSER_ID, sale_order_id, context=context)
        if 'nobill' in order.buy_way:
            return {'recall': False, 'message': ''}
        else:
            return super(WebsiteSale, self).payment_get_status(sale_order_id, **post)

    def checkout_form_validate(self, data):
        self.set_custom_mandatory_fields()
        return super(WebsiteSale, self).checkout_form_validate(data)

    def checkout_parse(self, address_type, data, remove_prefix=False):
        self.set_custom_mandatory_fields()
        return super(WebsiteSale, self).checkout_parse(address_type, data, remove_prefix)

    def set_custom_mandatory_fields(self):
        order = request.website.sale_get_order(force_create=1, context=request.context)
        if order.buy_way:
            if 'nobill_noship' in order.buy_way:
                website_sale.mandatory_billing_fields = ["name", "phone", "email"]
                website_sale.mandatory_shipping_fields = ["name", "phone", "email"]
            elif 'bill_noship' in order.buy_way:
                website_sale.mandatory_billing_fields = ["name", "phone", "email", "country_id"]
                website_sale.mandatory_shipping_fields = ["name", "phone", "email", "country_id"]
            else:
                website_sale.mandatory_billing_fields = ["name", "phone", "email", "street2", "city", "country_id"]
                website_sale.mandatory_shipping_fields = ["name", "phone", "street", "city", "country_id"]
        else:
            # Means no one radio button on cart form. Use regular variant.
            order.buy_way = 'bill_ship'
        return
