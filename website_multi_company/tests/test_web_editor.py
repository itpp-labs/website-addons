# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo.tests.common import HttpCase


class TestWebsiteEditor(HttpCase):
    at_install = True
    post_install = True

    def test_web_editor(self):
        """Test that Make Multi-Website is visible when needed"""

        tour = "website_multi_company.web_editor.tour"
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web_tour.tour']" ".run('%s')" % tour,
            "odoo.__DEBUG__.services['web_tour.tour']" ".tours['%s'].ready" % tour,
            login="admin",
        )
