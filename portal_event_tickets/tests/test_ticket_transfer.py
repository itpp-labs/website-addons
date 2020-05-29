# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from ..controllers.main import PortalEvent
from .common import TourCase


class TicketTransfer(TourCase):
    def test_ticket_transfer_tour(self):
        """user_portal1 transfers his ticket1 to user_portal2"""

        self.assertEqual(
            self.ticket1.attendee_partner_id,
            self.user_portal1.partner_id,
            "Wrong attendee_partner_id value before the test",
        )

        # user_portal1 transfers ticket to user_portal2
        env = self.env["res.users"].sudo(self.user_portal1).env
        PortalEvent()._ticket_transfer(env, self.user_portal2.email, self.ticket1.id)

        # user_portal2 click on the link in email
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('ticket_transfer_receive')",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.ticket_transfer_receive.ready",
            login=self.user_portal2.login,
        )
        self.assertEqual(
            self.ticket1.state,
            "open",
            "Ticket doesn't have state Confirmed after transfering",
        )

        self.assertEqual(
            self.ticket1.attendee_partner_id,
            self.user_portal2.partner_id,
            "Ticket Attendee was not changed",
        )
