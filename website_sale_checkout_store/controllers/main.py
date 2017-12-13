# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class WebsiteSaleExtended(WebsiteSale):

    @http.route()
    def address(self, **post):
        address_super = super(WebsiteSaleExtended, self).address(**post)
        address_super.qcontext.update(request.website.sale_get_order().get_shipping_billing())
        return address_super

    @http.route()
    def checkout(self, **post):
        order = request.website.sale_get_order()
        checkout_super = super(WebsiteSaleExtended, self).checkout(**post)
        try:
            order.buy_way = post['buyMethod']
        except:
            pass
        if not checkout_super.location:
            # no need to update variables if super does a redirection
            if str(order.buy_way) == "nobill_noship":
                # in nobill_noship case omits checkout page step and redirects to shop/payment
                # which in nobill case resets website order data and redirects to confirmation
                return request.redirect('/shop/payment')
            checkout_super.qcontext.update(order.get_shipping_billing())
        return checkout_super

    @http.route()
    def payment(self, **post):
        order = request.website.sale_get_order()
        if order.buy_way and 'nobill' in order.buy_way:
            request.session['sale_last_order_id'] = order.id
            order.force_quotation_send()
            request.website.sale_reset()
            return request.redirect('/shop/confirmation')
        else:
            return super(WebsiteSaleExtended, self).payment()

    @http.route()
    def payment_get_status(self, sale_order_id, **post):
        order = request.env['sale.order'].sudo().browse(sale_order_id)
        if order.buy_way and'nobill' in order.buy_way:
            return {'recall': False, 'message': ''}
        else:
            return super(WebsiteSaleExtended, self).payment_get_status(sale_order_id, **post)

    def _get_mandatory_fields(self):
        order = request.website.sale_get_order()
        if not order.buy_way or 'nobill' not in order.buy_way and 'noship' not in order.buy_way:
            return ["name", "phone", "email", "street", "city", "country_id"]
        elif 'noship' in order.buy_way:
            if 'nobill' in order.buy_way:
                return ["name", "phone", "email"]
            else:
                return ["name", "phone", "email", "country_id"]
        else:
            return ["name", "phone", "email", "street", "city"]

    def _get_mandatory_billing_fields(self):
        return self._get_mandatory_fields()

    def _get_mandatory_shipping_fields(self):
        return self._get_mandatory_fields()
