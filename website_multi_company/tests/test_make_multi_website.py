# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo.tests.common import TransactionCase

THEME_MODULE = "theme_module"


class TestCreate(TransactionCase):
    at_install = True
    post_install = True

    def _create_view(self, xml_id, arch):
        module, name = xml_id.split(".")
        view = self.env["ir.ui.view"].create(
            {"arch": arch, "key": xml_id, "type": "qweb"}
        )
        self.env["ir.model.data"].create(
            {"name": name, "model": "ir.ui.view", "module": module, "res_id": view.id}
        )
        return view

    def test_make_multi_website(self):
        """Test that original has copies after calling make_multi_website"""
        view = self._create_view(
            "%s.view" % THEME_MODULE,
            """<?xml version="1.0"?>
<t t-name="view" name="view">
<div>OK</div>
</t>
            """,
        )
        view.make_multi_website()

        self.assertFalse(view.active, "Converted view is still active")
        self.assertTrue(view.multitheme_copy_ids, "Converted view doesn't have copies")
