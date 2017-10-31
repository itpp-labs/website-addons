# -*- coding: utf-8 -*-
import logging
import time

from odoo.tests.common import HttpCase


_logger = logging.getLogger(__name__)


class TestBackend(HttpCase):
    at_install = False
    post_install = True

    def reset_demo(self):
        # other modules may override this data
        self.env['event.event'].search([]).write({
            'create_partner': True,
            'attendee_field_ids': [(6, 0, [
                self.env.ref('website_event_attendee_fields.attendee_field_name').id,
                self.env.ref('website_event_attendee_fields.attendee_field_email').id,
                self.env.ref('website_event_attendee_fields.attendee_field_phone').id,
                self.env.ref('website_event_attendee_fields.attendee_field_country_id').id,
                self.env.ref('website_event_attendee_fields.attendee_field_function').id,
            ])]
        })

    # FIXME: test is not passed in automatic mode, but works when tour runs manually
    def _test_base(self):
        self.reset_demo()
        self.phantom_js(
            '/event',

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('website_event_attendee_fields_test_tour_base', 2000)",

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.website_event_attendee_fields_test_tour_base.ready",

            login='demo',
            timeout=120,
        )
        time.sleep(5)  # wait few second to finish last request in the tour. TODO: check it via tour

        att1_email = "att1@example.com"
        att1_function = "JOB1"
        att1 = self.env['res.partner'].search([('email', '=', att1_email)])
        self.assertTrue(att1, 'Partner for attendee #1 is not created')
        self.assertEqual(att1.function, att1_function, 'Field "Function" is not saved at partner')

        registration = self.env['event.registration'].search([('partner_id', '=', att1.id)])
        self.assertTrue(registration, 'Registration for attendee #1 is not created')
