# -*- coding: utf-8 -*-
import odoo.tests


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):
    def test_open_url(self):
        self.phantom_js('/web/login', "", "", login='admin', timeout=240)
