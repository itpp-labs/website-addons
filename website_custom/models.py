# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID
from odoo import http
from odoo.http import request


class WebsiteCustom(http.Controller):

    @http.route(['/website_custom/ribbons'], type='json', auth="public", website=True)
    def ribbons(self, ids):
        cr = request.cr
        uid = SUPERUSER_ID
        res = request.registry['product.product'].search_read(domain=[('default_code', 'in', ids)], fields=['id', 'website_style_ids', 'default_code'])

        return res
