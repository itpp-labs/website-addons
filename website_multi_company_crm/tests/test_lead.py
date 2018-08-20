# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.tests.common import TransactionCase


THEME_MODULE = 'theme_module'


class TestRender(TransactionCase):
    at_install = True
    post_install = True

    def setUp(self):
        super(TestRender, self).setUp()
        self.website = self.env.ref('website.website2')
        self.company = self.env['res.company'].create({
            'name': 'New Test Website'
        })
        self.website.company_id = self.company

    def test_new_lead_context(self):
        lead = self.env['crm.lead'].with_context(
            website_id=self.website.id,
        ).create({
            'name': 'Test Lead',
        })
        self.assertEqual(lead.website_id, self.website, 'Incorrect Website value')
        self.assertEqual(lead.company_id, self.company, 'Incorrect Website value')

    def test_new_lead_backend(self):
        # add website to allowed
        self.env.user.backend_website_ids = [(4, self.website.id)]
        # switch current Website
        self.env.user.backend_website_id = self.website
        lead = self.env['crm.lead'].create({
            'name': 'Test Lead',
        })
        self.assertEqual(lead.website_id, self.website, 'Incorrect Website value')
        self.assertEqual(lead.company_id, self.company, 'Incorrect Website value')
