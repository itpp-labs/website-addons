# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from .common import TourCase


class TicketChange(TourCase):
    def test_ticket_change_tour(self):

        sale_order_count = self.env["sale.order"].search_count([])
        event_registration_count = self.env["event.registration"].search_count([])
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web_tour.tour']" ".run('ticket_change')",
            "odoo.__DEBUG__.services['web_tour.tour']" ".tours.ticket_change.ready",
            login=self.user_portal1.login,
        )

        self.assertEqual(
            sale_order_count + 1,
            self.env["sale.order"].search_count([]),
            "Sale order was not created after running tour",
        )
        self.assertEqual(
            event_registration_count + 1,
            self.env["event.registration"].search_count([]),
            "Ticket was not created after running tour",
        )

        order = self.env["sale.order"].search([], order="id desc", limit=1)
        ticket = self.env["event.registration"].search([], order="id desc", limit=1)

        order.action_confirm()
        self.assertEqual(
            self.ticket1.state,
            "cancel",
            "Old ticket %s was not canceled after refund" % self.ticket1.id,
        )
        self.assertEqual(
            ticket.state,
            "open",
            "New ticket is not confirmed after confirming the order",
        )
