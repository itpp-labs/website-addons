# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID
from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale as controller


class WebsiteSale(controller):

    @http.route(['/shop/checkout'], type='http', auth='public', website=True)
    def checkout(self, contact_name=None, email_from=None, phone=None):
        post = {
            'contact_name': contact_name or email_from,
            'email_from': email_from,
            'phone': phone,
        }

        error = set(field for field in ['email_from']
                    if not post.get(field))

        values = dict(post, error=error)
        if error:
            return request.website.render("website_sale.checkout", values)

        # find or create partner
        partner_obj = request.registry['res.partner']

        partner_id = partner_obj.search(request.cr, SUPERUSER_ID, [('email', '=', values['email_from'])])
        if partner_id:
            partner_id = partner_id[0]
            partner = partner_obj.browse(request.cr, SUPERUSER_ID, partner_id)
            values = {}
            for pk, k in [('name', 'contact_name'), ('phone', 'phone')]:
                if post[k]:
                    values[pk] = post[k]
            if values:
                partner.write(values)
        else:
            partner_id = partner_obj.create(request.cr, SUPERUSER_ID,
                                            {'name': values['contact_name'],
                                             'email': values['email_from'],
                                             'phone': values['phone'],
                                             })

        order = request.website.sale_get_order()
        # order_obj = request.registry.get('sale.order')
        order.write({'partner_id': partner_id})

        # send email
        cr = request.cr
        uid = request.uid
        context = request.context
        ir_model_data = request.registry['ir.model.data']
        template_id = ir_model_data.get_object_reference('website_sale_order', 'email_template_checkout')[1]
        email_ctx = dict(context)
        email_ctx.update({
            'default_model': 'sale.order',
            'default_res_id': order.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })
        composer_values = {}
        public_id = request.website.user_id.id
        if uid == public_id:
            composer_values['email_from'] = request.website.user_id.company_id.email
        composer_id = request.registry['mail.compose.message'].create(composer_values)
        request.registry['mail.compose.message'].send_mail([composer_id])

        request.website.sale_reset(context=context)
        return request.redirect('/shop/ready')

    @http.route(['/shop/ready'], type='http', auth='public', website=True)
    def shop_ready(self):
        values = {}
        return request.website.render('website_sale_order.ready', values)
