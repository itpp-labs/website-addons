# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# Copyright 2016-2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2017 Artyom Losev
# License AGPL <http://www.gnu.org/licenses/>.

import logging

from odoo import http
from odoo.http import request
import json

_logger = logging.getLogger(__name__)


class BarcodeController(http.Controller):

    @http.route(['/barcode/web/'], type='http', auth='user')
    def a(self, debug=False, **kw):
        if not request.session.uid:
            return http.local_redirect('/web/login?redirect=/barcode/web')

        context = {
            'session_info': json.dumps(request.env['ir.http'].session_info())
        }
        return request.render('stock_picking_barcode.barcode_index', qcontext=context)
