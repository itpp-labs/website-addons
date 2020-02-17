# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo.tests.common import TransactionCase

THEME_MODULE = "theme_module"


class TestRender(TransactionCase):
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

    def _search_view(self, xml_id, website):
        View = self.env["ir.ui.view"].with_context(active_test=False)
        # Get website-specific view if possible
        return View.search([("website_id", "=", website.id), ("key", "=", xml_id)])

    def _render(self, template, website):
        """It's similar to request.render(), but doesn't require to have "request" variable"""
        qcontext = {}
        return (
            self.env["ir.ui.view"]
            .with_context(website_id=website.id)
            .render_template(template, qcontext)
        )

    def test_render(self):
        VIEW_TEXT = "VIEW_1TEXT"
        VIEW_TEXT2 = "VIEW_2TEXT"

        # create view
        xml_id = "%s.view" % THEME_MODULE
        view = self._create_view(
            xml_id,
            """<?xml version="1.0"?>
            <t t-name="view" name="test view">
            <div>PLACEHOLDER</div>
            </t>""",
        )

        # add view to asset_ids ("Views") field of the default theme
        default_theme = self.env.ref("website_multi_theme.theme_default")
        self.env["website.theme.asset"].create(
            {"name": xml_id, "theme_id": default_theme.id}
        )

        # reload themes
        self.env["res.config.settings"].multi_theme_reload()

        # find copies of the views
        website = self.env.ref("website.default_website")
        website2 = self.env.ref("website.website2")

        view = self._search_view(xml_id, website)
        view2 = self._search_view(xml_id, website2)

        # replace text in each copy
        for v, text in [(view, VIEW_TEXT), (view2, VIEW_TEXT2)]:
            v.arch = v.arch.replace("PLACEHOLDER", text)

        # check that request.render uses proper copy of the
        for w, text in [(website, VIEW_TEXT), (website2, VIEW_TEXT2)]:
            result = self._render(xml_id, w)
            result = str(result)
            self.assertFalse(
                "PLACEHOLDER" in result,
                "Render uses original view, instead of copied one",
            )
            self.assertTrue(
                text in result,
                "Rendered template doesn't have updated text. Result:%s\nExpected:%s"
                % (result, text),
            )
