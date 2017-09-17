# -*- coding: utf-8 -*-
from odoo.tests import common


class TestDomainUpdating(common.HttpCase):
    at_install = False
    post_install = True

    def test_authenticate(self):
        """Copy-paste from addons/base/tests/test_xmlrpc.py"""
        db_name = common.get_db_name()
        uid = self.xmlrpc_common.login(db_name, 'admin', 'admin')
        self.assertEqual(uid, 1)
