# Copyright 2019 Denis Mudarisov <https://it-projects.info/team/trojikman>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests import tagged, HttpCase


@tagged('post_install', 'at_install')
class TestUi(HttpCase):
    def test_open_url(self):
        self.browser_js(
            '/',
            "odoo.__DEBUG__.services['web_tour.tour'].run('website_login_background_check')",
            "odoo.__DEBUG__.services['web_tour.tour'].tours.website_login_background_check.ready",
            login=None,
        )
