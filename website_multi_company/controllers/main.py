# -*- coding: utf-8 -*-
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.controllers.main import Website


class WebsiteSaleExtended(WebsiteSale):

    def _get_search_domain(self, *args, **kwargs):
        domain = super(WebsiteSaleExtended, self)._get_search_domain(*args, **kwargs)
        company = request.website.company_id
        if not company:
            return domain
        return ['|', ('company_id', '=', company.id), ('company_id', '=', False)] + domain


class WebsiteExtended(Website):

    @http.route()
    def index(self, **kw):
        website = request.website
        main_menu = request.env['website.menu'].search([
            ('website_id', '=', website.id),
            ('parent_id', '=', False)
        ], limit=1)
        if main_menu:
            first_menu = main_menu.child_id and main_menu.child_id[0]
            if first_menu:
                if first_menu.url and (not (first_menu.url.startswith(('/page/', '/?', '/#')) or (first_menu.url == '/'))):
                    return request.redirect(first_menu.url)
                if first_menu.url and first_menu.url.startswith('/page/'):
                    return request.env['ir.http'].reroute(first_menu.url)

        page = 'homepage' + str(website.id)
        full_page = 'website.' + page
        try:
            request.website.get_template(page)
        except ValueError:
            view = request.website.get_template('homepage')
            view_copy = view.sudo().copy({
                'website_id': website.id,
                'key': full_page,
            })
            request.env['ir.model.data'].sudo().create({
                'name': page,
                'model': 'ir.ui.view',
                'module': 'website',
                'res_id': view_copy.id,
            })
            # redirect to make commit
            request.redirect('/')

        return self.page(page)

    @http.route()
    def page(self, page, **opt):
        response = super(WebsiteExtended, self).page(page, **opt)
        uid = request.session.uid
        user = request.env['res.users'].browse(uid)
        response.qcontext.update({
            'editable': user and (not user.editor_website_ids or request.website.id in user.editor_website_ids.ids),
        })
        return response
