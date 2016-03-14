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
            acquirer_id = 1
            transaction_obj = request.registry.get('payment.transaction')
            tx_id = transaction_obj.create(cr, SUPERUSER_ID, {
                'acquirer_id': acquirer_id,
                'type': 'form',
                'amount': order.amount_total,
                'currency_id': order.pricelist_id.currency_id.id,
                'partner_id': order.partner_id.id,
                'partner_country_id': order.partner_id.country_id.id,
                'reference': request.env['payment.transaction'].get_next_reference(order.name),
                'sale_order_id': order.id,
            }, context=context)
            request.session['sale_transaction_id'] = tx_id
            tx = transaction_obj.browse(cr, SUPERUSER_ID, tx_id, context=context)
            # update quotation
            request.registry['sale.order'].write(
                cr, SUPERUSER_ID, [order.id], {
                    'payment_acquirer_id': acquirer_id,
                    'payment_tx_id': request.session['sale_transaction_id']
                }, context=context)
            # confirm the quotation
            if tx.acquirer_id.auto_confirm == 'at_pay_now':
                request.registry['sale.order'].action_confirm(cr, SUPERUSER_ID, [order.id], context=dict(request.context, send_email=True))
            order.with_context(dict(context, send_email=True)).action_confirm()
            request.website.sale_reset(context=context)
            return request.redirect('/shop/confirmation')
        else:
            return super(website_sale, self).payment()

    @http.route(['/shop/confirmation'], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        """ End of checkout process controller. Confirmation is basically seing
        the status of a sale.order. State at this point :

         - should not have any context / session info: clean them
         - take a sale.order id, because we request a sale.order and are not
           session dependant anymore
        """
        cr, uid, context = request.cr, request.uid, request.context

        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.registry['sale.order'].browse(cr, SUPERUSER_ID, sale_order_id, context=context)
        else:
            return request.redirect('/shop')
        return request.website.render("website_sale.confirmation", {'order': order})