# -*- coding: utf-8 -*-
import logging

from . import common


_logger = logging.getLogger(__name__)


class TestBackend(common.TestCase):

    def test_field(self):

        country_field = self.env.ref('website_event_attendee_fields.attendee_field_country_id')
        # cover name_get()
        _logger.info('name_get for country field: %s', country_field.display_name)

        country_field.domain = "[('code', '=', 'RU')]"

        self.assertEqual(1, len(country_field.get_select_options()))

        country_field.domain = False
        self.assertTrue(1 < len(country_field.get_select_options()))

    def test_registration(self):
        country = self.env.ref('base.ru')
        email_value = 'test@example.com'
        # emulate registration_confirm controller workflow
        registration_data = {
            'event_id': self.event,
            'name': 'Test',
            'email': email_value,
            'country_id': country.id,
        }
        registration = self.env['event.registration'].create(
            self.env['event.registration']._prepare_attendee_values(registration_data)
        )
        self.assertEqual(email_value, registration.email)
        self.assertEqual(email_value, registration.attendee_partner_id.email)
        self.assertEqual(country.id, registration.attendee_partner_id.country_id.id)

    def test_header(self):
        self.assertFalse(self.event.use_attendees_header)
        self.env.ref('website_event_attendee_fields.attendee_field_name').width = '3'
        self.env.ref('website_event_attendee_fields.attendee_field_email').width = '3'
        self.env.ref('website_event_attendee_fields.attendee_field_phone').width = '3'
        self.env.ref('website_event_attendee_fields.attendee_field_country_id').width = '3'
        self.event._compute_use_attendees_header()
        self.assertTrue(self.event.use_attendees_header)
