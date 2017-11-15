# -*- coding: utf-8 -*-
import odoo.tests


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):

    def test_checkout_nobill_noship(self):
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop_mandatory_fields_nobill_noship')",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.shop_mandatory_fields_nobill_noship.ready",
                        login=None)

    def test_checkout_bill_noship(self):
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop_mandatory_fields_bill_noship')",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.shop_mandatory_fields_bill_noship.ready",
                        login=None)

    def test_checkout_bill_ship(self):
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop_mandatory_fields_bill_ship')",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.shop_mandatory_fields_bill_ship.ready",
                        login=None)

    def test_checkout_nobill_ship(self):
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop_mandatory_fields_nobill_ship')",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.shop_mandatory_fields_nobill_ship.ready",
                        login=None)
