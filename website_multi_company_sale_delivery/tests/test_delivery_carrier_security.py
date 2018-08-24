# -*- coding: utf-8 -*-
# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp.tests.common import TransactionCase


class TestDeliveryCarrierSecurity(TransactionCase):
    at_install = True
    post_install = True

    def setUp(self):
        super(TestDeliveryCarrierSecurity, self).setUp()
        self.website = self.env.ref('website.website2')
        self.company = self.env['res.company'].create({
            'name': 'New Test Website'
        })
        self.website.company_id = self.company

        self.user = self.env.ref('website_multi_company_sale_delivery.delivery_carrier_read_user')
        self.user.write({'company_ids': [(4, self.company.id)], 'company_id': self.env.ref("base.main_company").id})

        self.country = self.env.ref("base.us")
        self.state = self.env.ref("base.state_us_2")

        self.delivery_carrier = self.env.ref("delivery.delivery_carrier")
        self.delivery_carrier.write({
            'website_ids': [(4, self.website.id)],
            'country_ids': [(6, 0, [self.country.id])],
            'state_ids': [(6, 0, [self.state.id])],
        })
        other_carriers = self.env.ref("delivery.normal_delivery_carrier") + self.env.ref("delivery.free_delivery_carrier")
        other_carriers.write({'website_ids': [(4, self.env.ref('website.default_website').id)]})

    def test_get_website_sale_countries_and_states(self):
        countries = self.country.with_context(website_id=self.website.id).get_website_sale_countries(mode='shipping')
        states = self.country.with_context(website_id=self.website.id).get_website_sale_states(mode='shipping')
        self.assertEqual(countries, self.country)
        self.assertEqual(states, self.state)
