# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo.tests.common import TransactionCase


class TestCreate(TransactionCase):
    at_install = True
    post_install = True

    def test_create_partner(self):
        company = self.env["res.company"].create({"name": "Non default Company"})
        website = self.env.ref("website.website2")
        website.company_id = company
        Partner = self.env["res.partner"].with_context(website_id=website.id)
        p = Partner.create({"name": "Test"})

        # Default value in res.partner is computed via env['res.company']._company_default_get
        # _company_default_get is computed via env['res.users']._get_company()
        # _get_company is redefined in website_multi_company to use website_id from context
        self.assertEqual(
            p.company_id.id,
            company.id,
            "Partner creation ignore current website from context",
        )
