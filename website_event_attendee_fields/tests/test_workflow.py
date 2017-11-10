# -*- coding: utf-8 -*-
import logging

from odoo import api
from odoo.tests.common import HttpCase


_logger = logging.getLogger(__name__)


class TestBackend(HttpCase):
    # We cannot run it with post_install, because other modules on travis may change demo events
    # Also, other modules may install website_event_sale as dependency
    at_install = True
    post_install = False

    def test_base(self):
        self.phantom_js(
            '/event',

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('website_event_attendee_fields_test_tour_base', 1000)",

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.website_event_attendee_fields_test_tour_base.ready",

            login='demo',
            timeout=200,
        )
        # data in tours are saved (but not commited!) via different cursor. So, we have to use that one
        test_env = api.Environment(self.registry.test_cr, self.uid, {})

        att_email = "att2@example.com"
        att_function = "JOB2"

        registration = test_env['event.registration'].search([], order='id desc', limit=1)

        self.assertEqual(registration.partner_id.email, att_email, "Latest registration doesn't have correct partner's email")
        self.assertEqual(registration.partner_id.function, att_function, "Latest registration doesn't have correct partner's Job")
