from datetime import datetime, timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestCase(TransactionCase):
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
