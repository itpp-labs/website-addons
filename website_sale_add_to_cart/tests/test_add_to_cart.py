# -*- coding: utf-8 -*-

import odoo.tests


# post_install is False due to test incompatibility with website_sale_checkout_store
@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(False)
class TestUi(odoo.tests.HttpCase):

    def test_add_to_cart(self):
        # delay is added to be sure that all elements have been rendered properly
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop_add_to_cart', 500)",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.shop_add_to_cart.ready",
                        login='admin')
