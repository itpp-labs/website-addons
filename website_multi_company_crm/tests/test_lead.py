# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo.tests.common import TransactionCase


class TestLead(TransactionCase):
    at_install = True
    post_install = True

    def setUp(self):
        super(TestLead, self).setUp()
        self.website = self.env.ref("website.website2")
        self.company = self.env["res.company"].create({"name": "New Test Website"})
        self.website.company_id = self.company

    def test_new_lead_context(self):
        lead = (
            self.env["crm.lead"]
            .with_context(website_id=self.website.id,)
            .create({"name": "Test Lead"})
        )
        self.assertEqual(lead.website_id, self.website, "Incorrect Website value")
        self.assertEqual(lead.company_id, self.company, "Incorrect Company value")

    def test_new_lead_backend(self):
        # add website to allowed
        self.env.user.write(
            dict(
                backend_website_ids=[(4, self.website.id)],
                backend_website_id=self.website.id,
                company_id=self.company.id,
                company_ids=[(4, self.company.id)],
            )
        )
        lead = self.env["crm.lead"].create({"name": "Test Lead"})
        self.assertEqual(lead.website_id, self.website, "Incorrect Website value")
        self.assertEqual(lead.company_id, self.company, "Incorrect Company value")
