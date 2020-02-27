# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License MIT (https://opensource.org/licenses/MIT).
import logging

import requests

import odoo.tests
from odoo import api
from odoo.tests.common import PORT, HttpCase, get_db_name

_logger = logging.getLogger(__name__)


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestSaleGetOrder(HttpCase):
    def setUp(self):
        super(TestSaleGetOrder, self).setUp()

    def test_sale_get_order(self):
        phantom_env = api.Environment(self.registry.test_cr, self.uid, {})

        website1 = phantom_env.ref("website.default_website")
        website1.domain = "127.0.0.1"
        website2 = phantom_env.ref("website.website2")
        website2.domain = "localhost"

        product_template = phantom_env.ref(
            "product.product_product_11_product_template"
        )
        product_product = phantom_env.ref("product.product_product_11")
        product_attribute = phantom_env.ref("product.product_attribute_1")
        product_attribute_value = phantom_env.ref("product.product_attribute_value_1")
        attribute = "attribute-{}-{}".format(product_template.id, product_attribute.id)
        data = {
            "product_id": product_product.id,
            attribute: product_attribute_value.id,
            "add_qty": 1,
        }
        _logger.info(data)

        login = "demo"
        self.authenticate(login, login)

        count_so_before = phantom_env["sale.order"].sudo().search_count([])

        url = "http://127.0.0.1:%d/shop/cart/update" % PORT
        _logger.info(url)
        response = self.url_open(url, data=data, timeout=60)
        self.assertEqual(response.status_code, 200)
        so_last = phantom_env["sale.order"].search([], limit=1)
        self.assertEqual(so_last.website_id, website1)

        # setup a magic session_id that will be rollbacked
        self.session = odoo.http.root.session_store.new()
        self.session_id = self.session.sid
        self.session.db = get_db_name()
        odoo.http.root.session_store.save(self.session)
        # setup an url opener helper
        self.opener = requests.Session()
        self.opener.cookies["session_id"] = self.session_id
        # authenticate
        self.authenticate(login, login)

        url = "http://localhost:%d/shop/cart/update" % PORT
        _logger.info(url)
        response = self.url_open(url, data=data, timeout=60)
        self.assertEqual(response.status_code, 200)
        so_last = phantom_env["sale.order"].search([], limit=1)
        self.assertEqual(so_last.website_id, website2)

        count_so_after = phantom_env["sale.order"].sudo().search_count([])
        self.assertEqual(count_so_after, count_so_before + 2)
