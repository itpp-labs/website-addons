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
            super(website_sale, self).payment(post)

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