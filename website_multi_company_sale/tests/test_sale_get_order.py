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

        website1 = phantom_env.ref('website.default_website')
        website1.domain = '127.0.0.1'
        website2 = phantom_env.ref('website.website2')
        website2.domain = 'localhost'

        product_template = phantom_env.ref('product.product_product_11_product_template')
        product_attribute = phantom_env.ref('product.product_attribute_1')
        product_attribute_value = phantom_env.ref('product.product_attribute_value_1')
        attribute = 'attribute-%s-%s' % (product_template.id, product_attribute.id)
        form_data = {
            'product_id': product_template.id,
            attribute: product_attribute_value.id,
            'add_qty': 1,
        }
        data = urllib.urlencode(form_data)

        login = "demo"
        self.authenticate(login, login)

        count_so_before = phantom_env['sale.order'].sudo().search_count([])

        response = self.url_open("http://127.0.0.1:%d/shop/cart/update" % PORT, data=data, timeout=60)
        self.assertEqual(response.getcode(), 200)

        # setup a magic session_id that will be rollbacked
        self.session = odoo.http.root.session_store.new()
        self.session_id = self.session.sid
        self.session.db = get_db_name()
        odoo.http.root.session_store.save(self.session)
        self.authenticate(login, login)

        headers = dict(self.opener.addheaders)
        headers['Cookie'] = 'session_id=%s' % self.session_id
        self.opener.addheaders = headers.items()

        response = self.url_open("http://localhost:%d/shop/cart/update" % PORT, data=data, timeout=60)
        self.assertEqual(response.getcode(), 200)

        count_so_after = phantom_env['sale.order'].sudo().search_count([])
        self.assertEqual(count_so_after, count_so_before+2)
