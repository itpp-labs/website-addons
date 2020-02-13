from . import common

USER_DEMO = "base.user_demo"


class TestCreate(common.TestCase):
    def test_create(self):
        """superuser creates registration for other person"""
        agent = self.env.user.partner_id

        registration = self.env["event.registration"].create(
            {
                "partner_id": agent.id,
                "event_id": self.event.id,
                "name": "Test",
                "email": "test@example.com",
            }
        )

        self.assertEqual(registration.partner_id.id, agent.id)
        self.assertTrue(
            registration.attendee_partner_id, "attendee_partner_id was not set"
        )
        self.assertNotEqual(registration.attendee_partner_id, agent.id)
