# -*- coding: utf-8 -*-
# Copyright 2017 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import odoo.tests
from odoo.api import Environment


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):

    def setUp(self):
        super(TestUi, self).setUp()
        cr = self.registry.cursor()
        assert cr == self.registry.test_cr
        env = Environment(cr, self.uid, {})
        module = 'product_tags'
        if env['ir.module.module'].search([('name', '=', module), ('state', '=', 'installed')]):
            tag = env['product.tag'].create({
                'name': 'iPod'
            })
            product = env['product.template'].search([('name', '=', 'iPod')])
            product.write({
                'tag_ids': [(6, 0, [tag.id])]
            })

    # big timeout due to long redirects (checkout -> confirmation) in nobill cases
    def test_checkout_nobill_noship(self):
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop_mandatory_fields_nobill_noship', 10000)",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.shop_mandatory_fields_nobill_noship.ready",
                        login=None, timeout=200)

    def test_checkout_bill_noship(self):
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop_mandatory_fields_bill_noship', 3000)",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.shop_mandatory_fields_bill_noship.ready",
                        login=None, timeout=200)

    def test_checkout_bill_ship(self):
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop_mandatory_fields_bill_ship', 3000)",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.shop_mandatory_fields_bill_ship.ready",
                        login=None, timeout=200)

    def test_checkout_nobill_ship(self):
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop_mandatory_fields_nobill_ship', 10000)",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.shop_mandatory_fields_nobill_ship.ready",
                        login=None, timeout=200)
