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
    def page(self, page, **opt):
        response = super(WebsiteExtended, self).page(page, **opt)
        uid = request.session.uid
        user = request.env['res.users'].browse(uid)
        response.qcontext.update({
            'editable': user and (not user.editor_website_ids or request.website.id in user.editor_website_ids.ids),
        })
        return response
