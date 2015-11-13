# -*- coding: utf-8 -*-
from openerp import http
from random import choice
from openerp.addons.web.controllers.main import Home
from openerp.http import request


class Background(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        pictures = request.env['ir.attachment'].search([
            ('use_as_background', '=', True)])
        if pictures:
            picture_url = r'/web/binary/saveas?id=' + \
                          str(choice(pictures.mapped('id'))) + \
                          r'&model=ir.attachment&field=datas&fieldname_field=datas_fname'
            request.params['picture_url'] = picture_url

        return super(Background, self).web_login(**kw)
