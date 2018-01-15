# -*- coding: utf-8 -*-
from odoo.http import request
from odoo.addons.website_portal.controllers.main import website_account


class MultiCompanyPortal(website_account):

    def _prepare_portal_layout_values(self):
        company = request.website.company_id
        user = request.env.user
        if user.company_id != company:
            update_company = True
            if company in user.company_ids:
                pass
            elif user.has_group('base.group_user'):
                # User is internal and doesn't have access to that company
                update_company = False
            else:
                # User is a portal user -- update his allowed companie
                user.write({
                    'company_ids': [(4, company.id, 0)]
                })

            if update_company:
                user.company_id = company

        return super(MultiCompanyPortal, self)._prepare_portal_layout_values()
