# -*- coding: utf-8 -*-
from odoo.http import request
from odoo.addons.website_portal.controllers.main import website_account


class MultiCompanyPortal(website_account):

    def _prepare_portal_layout_values(self):
        company = request.website.company_id
        user = request.env.user
        user.switch_multi_company(company)
        return super(MultiCompanyPortal, self)._prepare_portal_layout_values()
