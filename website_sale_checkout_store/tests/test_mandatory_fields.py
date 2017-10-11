# -*- coding: utf-8 -*-
import odoo.tests


@odoo.tests.common.at_install(False)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):
    print "====================================START=================================="

    def test_checkout(self):
        print "______________________before_Phantom_JS______________________________________"
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop_buy_product')",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.shop_buy_product.ready", login=None)
        print "====================================END===================================="
