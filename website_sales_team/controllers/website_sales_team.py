# -*- coding: utf-8 -*-
import werkzeug

from odoo import SUPERUSER_ID
from odoo import http
from odoo.http import request
from odoo.addons.website.models.website import slug

from odoo.addons.website_sale.controllers.main import QueryURL, table_compute, PPG, PPR, WebsiteSale as controller


class WebsiteSale(controller):

    @http.route([
        '/seller/<model("crm.case.section"):seller>'
    ], type='http', auth="public", website=True)
    def seller(self, seller):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        seller = pool.get('crm.case.section').browse(int(seller))
        values = {
            'seller': seller,
        }

        return request.website.render("website_sales_team.seller", values)

    @http.route(['/shop',
                 '/shop/<model("crm.case.section"):seller>',
                 '/shop/page/<int:page>',
                 '/shop/category/<model("product.public.category"):category>',
                 '/shop/category/<model("product.public.category"):category>/page/<int:page>'
                 ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', seller=None, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        domain = request.website.sale_product_domain()
        if search:
            for srch in search.split(" "):
                domain += ['|', '|', '|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                           ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch)]
        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

        if seller:
            domain += [('section_id', '=', int(seller))]

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attrib_set = set([v[1] for v in attrib_values])

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]

        keep = QueryURL('/shop', category=category and int(category), search=search, seller=seller and int(seller), attrib=attrib_list)

        if not context.get('pricelist'):
            pricelist = self.get_pricelist()
            context['pricelist'] = int(pricelist)
        else:
            pricelist = pool.get('product.pricelist').browse(context['pricelist'], context)

        product_obj = pool.get('product.template')

        url = "/shop"
        product_count = product_obj.search_count(domain)
        if search:
            post["search"] = search
        if category:
            category = pool['product.public.category'].browse(int(category))
            url = "/shop/category/%s" % slug(category)
        pager = request.website.pager(url=url, total=product_count, page=page, step=PPG, scope=7, url_args=post)
        product_ids = product_obj.search(domain, limit=PPG, offset=pager['offset'], order='website_published desc, website_sequence desc')
        products = product_obj.browse(product_ids)

        style_obj = pool['product.style']
        style_ids = style_obj.search([])
        styles = style_obj.browse(style_ids)

        category_obj = pool['product.public.category']
        category_ids = category_obj.search([('parent_id', '=', False)])
        categs = category_obj.browse(category_ids)

        attributes_obj = request.registry['product.attribute']
        attributes_ids = attributes_obj.search([])
        attributes = attributes_obj.browse(attributes_ids)

        from_currency = pool.get('product.price.type')._get_field_currency('list_price', context)
        to_currency = pricelist.currency_id
        compute_currency = lambda price: pool['res.currency']._compute(from_currency, to_currency, price)

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'products': products,
            'bins': table_compute().process(products),
            'rows': PPR,
            'styles': styles,
            'categories': categs,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'style_in_product': lambda style, product: style.id in [s.id for s in product.website_style_ids],
            'attrib_encode': lambda attribs: werkzeug.url_encode([('attrib', i) for i in attribs]),
        }
        return request.website.render("website_sale.products", values)

    @http.route(['/shop/checkout'], type='http', auth='public', website=True)
    def checkout(self, contact_name=None, email_from=None, phone=None):
        cr = request.cr
        uid = request.uid
        context = request.context

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
            partner = partner_obj.browse(partner_id)
            values = {}
            for pk, k in [('name', 'contact_name'), ('phone', 'phone')]:
                if post[k]:
                    values[pk] = post[k]
            if values:
                partner.write(values)
        else:
            partner_id = partner_obj.create(request.cr, SUPERUSER_ID,
                                            {'name': values['contact_name'],
                                             'email': values['email_from']})

        order = request.website.sale_get_order()
        # order_obj = request.registry.get('sale.order')
        order.write({'partner_id': partner_id})

        section_ids = {}
        for line in order.order_line:
            if not line.product_id.section_id:
                continue
            id = line.product_id.section_id.id
            if id not in section_ids:
                section_ids[id] = []
            section_ids[id].append(line)

        order_ids = []
        for section_id, lines in section_ids.iteritems():
            order_id = order.copy({'parent_id': order.id, 'section_id': section_id, 'order_line': [(5, 0, 0)]})
            for line in lines:
                line.copy({'order_id': order_id.id})
        request.registry.get('sale.order').signal_workflow(order_ids, 'quotation_sent')
        request.registry.get('sale.order').signal_workflow([order.id], 'cancel')
        # send email
        ir_model_data = request.registry['ir.model.data']
        template_id = ir_model_data.get_object_reference('website_sales_team', 'email_template_checkout')[1]
        email_ctx = dict(context)
        email_ctx.update({
            'default_model': 'sale.order',
            'default_res_id': order.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            # 'mark_so_as_sent': True
        })
        composer_values = {}
        public_id = request.website.user_id.id
        if uid == public_id:
            composer_values['email_from'] = request.website.user_id.company_id.email
        composer_id = request.registry['mail.compose.message'].create(composer_values)
        request.registry['mail.compose.message'].send_mail([composer_id])

        request.website.sale_reset(context=context)
        return request.redirect('/shop/ready')
