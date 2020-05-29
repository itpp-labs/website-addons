# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
import logging

from ..controllers.main import WebsiteEventControllerExtended
from . import common

_logger = logging.getLogger(__name__)


class TestBackend(common.TestCase):
    def test_field(self):

        country_field = self.env.ref(
            "website_event_attendee_fields.attendee_field_country_id"
        )
        # cover name_get()
        _logger.info("name_get for country field: %s", country_field.display_name)

        country_field.domain = "[('code', '=', 'RU')]"

        self.assertEqual(1, len(country_field.get_select_options()))

        country_field.domain = False
        self.assertTrue(1 < len(country_field.get_select_options()))

    def test_registration(self):
        country = self.env.ref("base.ru")
        email_value = "test@example.com"
        self.assertFalse(
            self.env["res.partner"].search([("email", "=", email_value)]),
            "Tests assumed, that partner with email %s doesn't exist" % email_value,
        )
        # emulate registration_confirm controller workflow
        registration_data = {
            "event_id": self.event,
            "name": "Test",
            "email": email_value,
            "country_id": country.id,
        }
        registration = self.env["event.registration"].create(
            self.env["event.registration"]._prepare_attendee_values(registration_data)
        )
        self.assertEqual(email_value, registration.email)
        self.assertEqual(email_value, registration.attendee_partner_id.email)
        self.assertEqual(country.id, registration.attendee_partner_id.country_id.id)

    def test_header(self):
        self.assertFalse(self.event.use_attendees_header)
        self.env.ref("website_event_attendee_fields.attendee_field_name").width = "3"
        self.env.ref("website_event_attendee_fields.attendee_field_email").width = "3"
        self.env.ref("website_event_attendee_fields.attendee_field_phone").width = "3"
        self.env.ref(
            "website_event_attendee_fields.attendee_field_country_id"
        ).width = "3"
        self.event._compute_use_attendees_header()
        self.assertTrue(self.event.use_attendees_header)

    def test_emails_duplicates(self):
        event = self.event.id
        email = "email@example.com"
        post = {
            "1-name": "dummy",
            "1-email": email,
            "1-country_id": 1,
            "2-name": "dummy",
            "2-email": email,
            "2-country_id": 1,
        }
        with self.assertRaises(AssertionError):
            obj = WebsiteEventControllerExtended()
            obj.registration_confirm(event, **post)
