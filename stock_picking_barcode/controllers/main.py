# -*- coding: utf-8 -*-
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
