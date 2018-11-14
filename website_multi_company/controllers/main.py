# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleExtended(WebsiteSale):

    def _get_search_domain(self, *args, **kwargs):
        domain = super(WebsiteSaleExtended, self)._get_search_domain(*args, **kwargs)
        company = request.website.company_id
        if not company:
            return domain
        return ['|', ('company_id', '=', company.id), ('company_id', '=', False)] + domain
