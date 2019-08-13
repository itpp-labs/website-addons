# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from datetime import datetime, timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestCase(TransactionCase):
    at_install = True
    post_install = True

    def setUp(self):
        super(TestCase, self).setUp()
        self.event = self.env["event.event"].create(
            {
                "name": "TestEvent",
                "attendee_signup": True,
                "create_partner": True,
                "date_begin": fields.Datetime.to_string(
                    datetime.today() + timedelta(days=1)
                ),
                "date_end": fields.Datetime.to_string(
                    datetime.today() + timedelta(days=15)
                ),
            }
        )
        self.event.write(
            {
                "attendee_field_ids": [
                    (
                        6,
                        0,
                        [
                            self.env.ref(
                                "website_event_attendee_fields.attendee_field_name"
                            ).id,
                            self.env.ref(
                                "website_event_attendee_fields.attendee_field_email"
                            ).id,
                            self.env.ref(
                                "website_event_attendee_fields.attendee_field_phone"
                            ).id,
                            self.env.ref(
                                "website_event_attendee_fields.attendee_field_country_id"
                            ).id,
                        ],
                    )
                ]
            }
        )
