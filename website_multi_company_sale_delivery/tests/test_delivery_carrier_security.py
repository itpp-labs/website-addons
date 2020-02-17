# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License MIT (https://opensource.org/licenses/MIT).
from odoo.tests.common import TransactionCase


class TestDeliveryCarrierSecurity(TransactionCase):
    at_install = True
    post_install = True

    def setUp(self):
        super(TestDeliveryCarrierSecurity, self).setUp()
        self.website = self.env.ref("website.website2")
        self.company = self.env["res.company"].create({"name": "New Test Website"})
        self.website.company_id = self.company

        self.user = self.env.ref(
            "website_multi_company_sale_delivery.delivery_carrier_read_user"
        )
        # self.user.write({'company_ids': [(4, self.company.id)], 'company_id': self.env.ref("base.main_company").id})
        self.user.write(
            {"company_ids": [(4, self.company.id)], "company_id": self.company.id}
        )

        self.country = self.env.ref("base.us")
        self.state = self.env.ref("base.state_us_2")

        self.delivery_carrier = self.env.ref("delivery.delivery_carrier")
        self.delivery_carrier.write(
            {
                "website_ids": [(4, self.website.id)],
                "country_ids": [(6, 0, [self.country.id])],
                "state_ids": [(6, 0, [self.state.id])],
            }
        )
        other_carriers = self.env.ref(
            "delivery.normal_delivery_carrier"
        ) + self.env.ref("delivery.free_delivery_carrier")
        other_carriers.write(
            {"website_ids": [(4, self.env.ref("website.default_website").id)]}
        )
        self.all_carriers = other_carriers + self.delivery_carrier
        self.all_carriers.write({"website_published": True})

    def test_get_website_sale_countries_and_states(self):
        countries = self.country.with_context(
            website_id=self.website.id
        ).get_website_sale_countries(mode="shipping")
        states = self.country.with_context(
            website_id=self.website.id
        ).get_website_sale_states(mode="shipping")
        self.assertEqual(countries, self.country)
        self.assertEqual(states, self.state)

    def test_get_delivery_carriers(self):

        # for frontend (there is website_id in context)
        delivery_carriers = (
            self.env["delivery.carrier"]
            .sudo(self.user)
            .with_context(website_id=self.website.id)
            .search([("website_published", "=", True)])
        )
        self.assertNotEqual(self.all_carriers, delivery_carriers)
        self.assertEqual(self.delivery_carrier, delivery_carriers)

        # for backend (no website_id in context and no backend_website_id in the user's settings either - all published carriers should get found
        self.user.backend_website_id = None
        delivery_carriers = (
            self.env["delivery.carrier"]
            .sudo(self.user)
            .search([("website_published", "=", True)])
        )
        self.assertEqual(self.all_carriers, delivery_carriers)
