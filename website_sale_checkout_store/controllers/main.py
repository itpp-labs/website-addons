# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class WebsiteSaleExtended(WebsiteSale):

    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        try:
            order.buy_way = post['buyMethod']
        except:
            pass

        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            return request.redirect('/shop/address')

        for f in self._get_mandatory_billing_fields():
            if not order.partner_id[f]:
                return request.redirect('/shop/address?partner_id=%d' % order.partner_id.id)

        values = self.checkout_values(**post)
        values['order'] = order
        sale_order_id = request.session.get('sale_order_id')
        request.env["sale.order"].browse(sale_order_id).sudo().payment_and_delivery_method_info()

        # Avoid useless rendering if called in ajax
        if post.get('xhr'):
            return 'ok'
        return request.render("website_sale.checkout", values)

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        order = request.website.sale_get_order()
        if 'nobill' in order.buy_way:
            order.force_quotation_send()
            request.website.sale_reset()
            return request.redirect('/shop/confirmation')
        else:
            return super(WebsiteSaleExtended, self).payment()

    @http.route('/shop/payment/get_status/<int:sale_order_id>', type='json', auth="public", website=True)
    def payment_get_status(self, sale_order_id, **post):
        order = request.env['sale.order'].browse(sale_order_id)
        if 'nobill' in order.buy_way:
            return {'recall': False, 'message': ''}
        else:
            return super(WebsiteSaleExtended, self).payment_get_status(sale_order_id, **post)

    def checkout_form_validate(self, *args, **kwargs):
        self.set_custom_mandatory_fields()
        return super(WebsiteSaleExtended, self).checkout_form_validate(*args, **kwargs)

    def checkout_parse(self, address_type, data, remove_prefix=False):
        self.set_custom_mandatory_fields()
        return super(WebsiteSaleExtended, self).checkout_parse(address_type, data, remove_prefix)

    def set_custom_mandatory_fields(self):
        order = request.website.sale_get_order(force_create=1)
        if order.buy_way:
            if 'nobill_noship' in order.buy_way:
                WebsiteSale.mandatory_billing_fields = ["name", "phone", "email"]
                WebsiteSale.mandatory_shipping_fields = ["name", "phone", "email"]
            elif 'bill_noship' in order.buy_way:
                WebsiteSale.mandatory_billing_fields = ["name", "phone", "email"]
                WebsiteSale.mandatory_shipping_fields = ["name", "phone", "email"]
            else:
                WebsiteSale.mandatory_billing_fields = ["name", "phone", "email", "street2", "city", "country_id"]
                WebsiteSale.mandatory_shipping_fields = ["name", "phone", "street", "city", "country_id"]
        else:
            # Means regular variant.
            order.buy_way = 'bill_ship'
        return
