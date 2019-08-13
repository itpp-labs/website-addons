# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from datetime import datetime, timedelta

from odoo import fields
from odoo.tests.common import TransactionCase

USER_DEMO = "base.user_demo"


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

    def test_self_registration(self):
        """demouser creates registration for himself"""
        agent = self.env.ref(USER_DEMO).partner_id
        NEW_NAME = "New DemoName"

        registration = self.env["event.registration"].create(
            {
                "partner_id": agent.id,
                "event_id": self.event.id,
                "name": NEW_NAME,
                "email": agent.email,
            }
        )

        self.assertEqual(
            registration.partner_id.id, agent.id, "Wrong Agent value",
        )
        self.assertEqual(
            registration.attendee_partner_id.id, agent.id, "Wrong Attendee value",
        )

        self.assertEqual(
            registration.attendee_partner_id.name,
            NEW_NAME,
            "User has a right to change attendee values, if he buy ticket for himself",
        )

    def test_registration_for_existing_user(self):
        """superuser creates registration for another user"""
        agent = self.env.user.partner_id
        NEW_NAME = "New Demo Name"

        attendee = self.env.ref(USER_DEMO)

        registration = self.env["event.registration"].create(
            {
                "partner_id": agent.id,
                "event_id": self.event.id,
                "name": NEW_NAME,
                "email": attendee.email,
            }
        )

        self.assertNotEqual(
            registration.attendee_partner_id.name,
            NEW_NAME,
            "Attendee's name must not be changed for security reasons",
        )
