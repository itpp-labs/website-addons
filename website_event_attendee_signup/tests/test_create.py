# -*- coding: utf-8 -*-
from . import common


class TestCreate(common.TestCase):

    def test_create(self):
        # create registration as Superuser
        agent = self.env.user.partner_id

        registration = self.env['event.registration'].create({
            'partner_id': agent.id,
            'event_id': self.event.id,
            'name': 'Test',
            'email': 'test@example.com',
        })

        self.assertEqual(
            registration.agent_id.id,
            agent.id
        )
        self.assertNotEqual(
            registration.partner_id.id,
            agent.id
        )
