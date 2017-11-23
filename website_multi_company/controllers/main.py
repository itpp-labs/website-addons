# -*- coding: utf-8 -*-
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleExtended(WebsiteSale):

    def _get_search_domain(self, *args, **kwargs):
        domain = super(WebsiteSaleExtended, self)._get_search_domain(*args, **kwargs)
        company = request.website.company_id
        if not company:
            return domain
        return [('company_id', '=', company.id)] + domain
