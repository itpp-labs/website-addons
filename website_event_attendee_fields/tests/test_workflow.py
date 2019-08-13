# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
import logging

from odoo import api
from odoo.tests.common import HttpCase

_logger = logging.getLogger(__name__)


class TestBackend(HttpCase):
    # Making post_install True requires to update demo data, because other modules may change them
    at_install = True
    post_install = False

    def test_base(self):
        att_email = "att2@example.com"
        att_function = "JOB2"

        # data in tours are saved (but not commited!) via different cursor. So, we have to use that one
        test_env = api.Environment(self.registry.test_cr, self.uid, {})

        partner = test_env["res.partner"].search([("email", "=ilike", att_email)])
        self.assertFalse(
            partner,
            "It's assumed that partner with email %s doesn't not exist" % att_email,
        )

        registration_count_before = test_env["event.registration"].search_count([])

        self.phantom_js(
            "/event",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('website_event_attendee_fields_test_tour_base', 1000)",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.website_event_attendee_fields_test_tour_base.ready",
            login="demo",
            timeout=200,
        )
        registration_count_after = test_env["event.registration"].search_count([])

        self.assertEqual(
            registration_count_before,
            registration_count_after - 2,
            "Amount of created registrations is not equal to 2",
        )

        registration = test_env["event.registration"].search(
            [], order="id desc", limit=1
        )

        _logger.debug(
            "registration_count_after=%s; registration: %s",
            registration_count_after,
            (registration, registration.partner_id, registration.partner_id.name),
        )
        self.assertTrue(
            registration.attendee_partner_id, "Latest registration doesn't have partner"
        )
        self.assertEqual(
            registration.attendee_partner_id.email,
            att_email,
            "Latest registration doesn't have correct partner's email",
        )
        self.assertEqual(
            registration.attendee_partner_id.function,
            att_function,
            "Latest registration doesn't have correct partner's Job",
        )
