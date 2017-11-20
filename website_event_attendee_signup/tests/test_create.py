# -*- coding: utf-8 -*-
from . import common


class TestCreate(common.TestCase):

    def test_create(self):
        """superuser creates registration for other person"""
        agent = self.env.user.partner_id

        registration = self.env['event.registration'].create({
            'partner_id': agent.id,
            'event_id': self.event.id,
            'name': 'Test',
            'email': 'test@example.com',
        })

        self.assertEqual(
            registration.partner_id.id,
            agent.id
        )
        self.assertTrue(
            registration.attendee_partner_id,
            "attendee_partner_id was not set"
        )
        self.assertNotEqual(
            registration.attendee_partner_id,
            agent.id
        )

    def test_registration_for_existing_user(self):
        """superuser creates registration for himself"""
        agent = self.env.user.partner_id
        NEW_NAME = 'New AdminName'

        registration = self.env['event.registration'].create({
            'partner_id': agent.id,
            'event_id': self.event.id,
            'name': NEW_NAME,
            'email': agent.email,
        })

        self.assertEqual(
            registration.partner_id.id,
            agent.id,
            "Wrong Agent value",
        )
        self.assertEqual(
            registration.attendee_partner_id.id,
            agent.id,
            "Wrong Attendee value",
        )

        self.assertNotEqual(
            registration.partner_id.name,
            NEW_NAME,
            "Contact's name must not be changed for security reasons",
        )
