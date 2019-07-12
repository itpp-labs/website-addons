# -*- coding: utf-8 -*-

import odoo.tests


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):

    def test_search_tags(self):
        # delay is added to be sure that all elements have been rendered properly
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('website_sale_search_tags', 500)",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.website_sale_search_tags.ready",
                        login='admin')
