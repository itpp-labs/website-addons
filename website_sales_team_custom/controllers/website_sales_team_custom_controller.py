# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID
from odoo import http
from odoo.http import request


class WebsiteSalesTeamCustomController(http.Controller):

    @http.route(['/calculator/currencies'], type='json', auth='public', website=True)
    def currencies(self, names, **post):
        currency_obj = request.registry.get('res.currency')
        ids = currency_obj.search(request.cr, SUPERUSER_ID, [('name', 'in', names)])
        res = []
        for c in currency_obj.browse(request.cr, SUPERUSER_ID, ids):
            res.append({
                'name': c.name,
                'symbol': c.symbol,
                # 'position': c.position,
                'rounding': c.rounding,
                'rate': c.rate,
            })
        return res
