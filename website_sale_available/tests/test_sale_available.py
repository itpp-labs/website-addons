
import odoo.tests


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):

    def test_sale_available(self):
        # delay is added to be sure that all elements have been rendered properly
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop_sale_available', 1000)",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.shop_sale_available.ready",
                        login='admin')
