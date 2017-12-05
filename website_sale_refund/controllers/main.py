# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleRefund(WebsiteSale):

    @http.route()
    def cart(self, **post):
        response = super(PortalEvent, self).cart(**post)
        if post.get('total_is_negative'):
            response.qcontext.update({
                'warning_msg': _('Total amount is negative. Please add more products'),
            })
        return response

    def checkout_redirection(self, order):
        if order.amount_total < 0 :
            return request.redirect('/shop/cart?total_is_negative=1')
        return super(PortalEvent, self).checkout_redirection(order)
