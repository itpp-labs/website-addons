# -*- coding: utf-8 -*-
import urlparse
import urllib

import odoo.tests
from odoo.tests.common import PORT, HttpCase, get_db_name
from odoo import api


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestSaleGetOrder(HttpCase):

    def setUp(self):
        super(TestSaleGetOrder, self).setUp()

    def test_sale_get_order(self):
        phantom_env = api.Environment(self.registry.test_cr, self.uid, {})
        demo_user = phantom_env.ref('base.user_demo')

        web_base_url = phantom_env['ir.config_parameter'].get_param('web.base.url') or base_location
        parse_result = urlparse.urlparse(web_base_url)
        netloc = parse_result.netloc

        website1 = phantom_env.ref('website.default_website')
        website1.domain = 'website1.' + netloc
        website2 = phantom_env.ref('website.website2')
        website2.domain = 'website2.' + netloc

        parse_result_list = list(parse_result)
        parse_result_list[1] = website1.domain
        url = urlparse.urlunparse(parse_result_list)

        form_data = {
            'product_id': 21,
            'attribute-18-1': 1,
            'add_qty': 1,
        }
        data = urllib.urlencode(form_data)

        login = "demo"
        self.authenticate(login, login)

        count_so_before = phantom_env['sale.order'].sudo().search_count([])
        count_so_before1 = phantom_env['sale.order'].sudo().search_count([])

        print '\n\n', 'count_so_before1', count_so_before1, '\n\n'
        # domain_name = request and request.httprequest.environ.get('HTTP_HOST', '').split(':')[0] or None
        self.opener.addheaders.append(('Host', website1.domain))
        print '\n\n', 'self.opener.addheaders', self.opener.addheaders, 'PORT', PORT, 'self.session', self.session, '\n\n'
        response = self.url_open("http://localhost:%d/shop/cart/update" % PORT, data=data, timeout=60)
        self.assertEqual(response.getcode(), 200)
        count_so_after1 = phantom_env['sale.order'].sudo().search_count([])
        print '\n\n', 'count_so_after1', count_so_after1, '\n\n'

        # setup a magic session_id that will be rollbacked
        self.session = odoo.http.root.session_store.new()
        self.session_id = self.session.sid
        self.session.db = get_db_name()
        odoo.http.root.session_store.save(self.session)
        self.authenticate(login, login)

        headers = dict(self.opener.addheaders)
        headers['Host'] = website2.domain
        headers['Cookie'] = 'session_id=%s' % self.session_id
        self.opener.addheaders = headers.items()
        print '\n\n', 'self.opener.addheaders', self.opener.addheaders, 'PORT', PORT, 'self.session', self.session, '\n\n'

        count_so_before2 = phantom_env['sale.order'].sudo().search_count([])
        print '\n\n', 'count_so_before2', count_so_before2, '\n\n'
        response = self.url_open("http://localhost:%d/shop/cart/update" % PORT, data=data, timeout=60)
        self.assertEqual(response.getcode(), 200)
        count_so_after2 = phantom_env['sale.order'].sudo().search_count([])
        print '\n\n', 'count_so_after2', count_so_after2, '\n\n'

        count_so_after = phantom_env['sale.order'].sudo().search_count([])
        self.assertEqual(count_so_after, count_so_before+2)
