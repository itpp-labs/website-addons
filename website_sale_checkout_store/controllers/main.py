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
        """ Payment step. This page proposes several payment means based on available
        payment.acquirer. State at this point :

         - a draft sale order with lines; otherwise, clean context / session and
           back to the shop
         - no transaction in context / session, or only a draft one, if the customer
           did go to a payment.acquirer website but closed the tab without
           paying / canceling
        """
        cr, uid, context = request.cr, request.uid, request.context
        payment_obj = request.registry.get('payment.acquirer')
        sale_order_obj = request.registry.get('sale.order')

        order = request.website.sale_get_order(context=context)

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        shipping_partner_id = False
        if order:
            if order.partner_shipping_id.id:
                shipping_partner_id = order.partner_shipping_id.id
            else:
                shipping_partner_id = order.partner_invoice_id.id

        values = {
            'website_sale_order': order
        }
        values['errors'] = sale_order_obj._get_errors(cr, uid, order, context=context)
        values.update(sale_order_obj._get_website_data(cr, uid, order, context))

        if not values['errors']:
            # find an already existing transaction
            tx = request.website.sale_get_transaction()
            acquirer_ids = payment_obj.search(cr, SUPERUSER_ID, [('website_published', '=', True), ('company_id', '=', order.company_id.id)], context=context)
            values['acquirers'] = list(payment_obj.browse(cr, uid, acquirer_ids, context=context))
            render_ctx = dict(context, submit_class='btn btn-primary', submit_txt=_('Pay Now'))
            for acquirer in values['acquirers']:
                acquirer.button = payment_obj.render(
                    cr, SUPERUSER_ID, acquirer.id,
                    tx and tx.reference or request.env['payment.transaction'].get_next_reference(order.name),
                    order.amount_total,
                    order.pricelist_id.currency_id.id,
                    values={
                        'return_url': '/shop/payment/validate',
                        'partner_id': shipping_partner_id,
                        'billing_partner_id': order.partner_invoice_id.id,
                    },
                    context=render_ctx)
        if 'nobill' in order.buy_way:
            request.website.sale_reset(context=context)
            return request.redirect('/shop/confirmation')
        return request.website.render("website_sale.payment", values)

    @http.route(['/shop/confirm_order'], type='http', auth="public", website=True)
    def confirm_order(self, **post):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry

        order = request.website.sale_get_order(context=context)
        if not order:
            return request.redirect("/shop")

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        values = self.checkout_values(post)

        values["error"], values["error_message"] = self.checkout_form_validate(values["checkout"])
        if values["error"]:
            order = request.website.sale_get_order(force_create=1, context=context)
            values['order'] = order
            return request.website.render("website_sale.checkout", values)
        self.checkout_form_save(values["checkout"])

        if not int(post.get('shipping_id', 0)):
            order.partner_shipping_id = order.partner_invoice_id

        request.session['sale_last_order_id'] = order.id

        request.website.sale_get_order(update_pricelist=True, context=context)

        extra_step = registry['ir.model.data'].xmlid_to_object(cr, uid, 'website_sale.extra_info_option', raise_if_not_found=True)
        if extra_step.active:
            return request.redirect("/shop/extra_info")

        return request.redirect("/shop/payment")