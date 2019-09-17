# Copyright 2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteMultiCompanySale(WebsiteSale):

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        response = super(WebsiteMultiCompanySale, self).shop(page=page, category=category, search=search, ppg=ppg, **post)
        categs = request.env['product.public.category'].search([
            ('parent_id', '=', False),
            '|',
            ('website_ids', '=', False),
            ('website_ids', 'in', [request.website.id]),
        ])
        response.qcontext.update({
            'categories': categs,
        })
        return response

    def values_postprocess(self, order, mode, values, errors, error_msg):
        new_values, errors, error_msg = super(WebsiteMultiCompanySale, self).\
            values_postprocess(order, mode, values, errors, error_msg)
        new_values['website_id'] = new_values['backend_website_id'] = request.website.id
        return new_values, errors, error_msg
