import re

from odoo.tests import common

from ..models.res_users import WEBSITE_RE, WEBSITE_REFS


class TestDomainUpdating(common.HttpCase):
    at_install = False
    post_install = True

    def test_authenticate(self):
        db_name = common.get_db_name()
        env = dict(base_location="http://build-123.runbot.example.com",)
        website_domains = {}
        for wref in WEBSITE_REFS:
            website = self.env.ref(wref, raise_if_not_found=False)
            m = re.search(WEBSITE_RE, website.domain)
            self.assertTrue(bool(m))
            key = m.group(1)
            website_domains[wref] = "build-123." + key + ".runbot.example.com"
        uid = self.registry["res.users"].authenticate(db_name, "admin", "admin", env)
        # since Odoo 12.0 admin user is 2
        self.assertEqual(uid, 2)

        for wref in WEBSITE_REFS:
            website = self.env.ref(wref, raise_if_not_found=False)
            self.assertEqual(website.domain, website_domains[wref])
