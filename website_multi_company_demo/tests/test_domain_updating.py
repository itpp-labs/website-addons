# -*- coding: utf-8 -*-
from odoo.tests import common


class TestDomainUpdating(common.HttpCase):
    at_install = False
    post_install = True

    def test_authenticate(self):
        db_name = common.get_db_name()
        env = dict(
            base_location="http://build-123.runbot.example.com",
        )
        uid = self.registry['res.users'].authenticate(db_name, 'admin', 'admin', env)
        self.assertEqual(uid, 1)
