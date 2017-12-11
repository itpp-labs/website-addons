# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class WebsiteSaleExtended(WebsiteSale):

    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        order = request.website.sale_get_order()
        try:
            order.buy_way = post['buyMethod']
        except:
            pass
        if order.buy_way:
            if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
                return request.redirect('/shop/address')
            sale_order_id = request.session.get('sale_order_id')
            if 'noship' in order.buy_way and 'nobill' in order.buy_way:
                request.session['sale_last_order_id'] = order.id
                request.website.sale_reset()
                return request.redirect('/shop/confirmation')
            request.env["sale.order"].browse(sale_order_id).sudo().payment_and_delivery_method_info()
        return super(WebsiteSaleExtended, self).checkout(**post)

    def checkout_values(self, **post):
        values = super(WebsiteSaleExtended, self).checkout_values(**post)
        order = request.website.sale_get_order()
        values['order'] = order
        return values

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        order = request.website.sale_get_order()
        if not order.buy_way:
            return super(WebsiteSaleExtended, self).payment()
        if 'nobill' in order.buy_way:
            order.force_quotation_send()
            request.website.sale_reset()
            return request.redirect('/shop/confirmation')
        else:
            return super(WebsiteSaleExtended, self).payment()

    @http.route('/shop/payment/get_status/<int:sale_order_id>', type='json', auth="public", website=True)
    def payment_get_status(self, sale_order_id, **post):
        order = request.env['sale.order'].sudo().browse(sale_order_id)
        if not order.buy_way:
            return super(WebsiteSaleExtended, self).payment_get_status(sale_order_id, **post)
        if 'nobill' in order.buy_way:
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
