# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from datetime import datetime, timedelta

import odoo
from odoo import api, fields
from odoo.tests.common import HttpCase


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TourCase(HttpCase):
    def setUp(self):
        super(TourCase, self).setUp()
        self.env = api.Environment(self.registry.test_cr, self.uid, {})

        # create Event
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
                "website_published": True,
            }
        )
        self.ticket_type_1 = self.env.ref("event_sale.event_0_ticket_1").copy(
            {"event_id": self.event.id}
        )
        self.ticket_type_2 = self.env.ref("event_sale.event_0_ticket_2").copy(
            {"event_id": self.event.id}
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
                            self.env.ref(
                                "website_event_attendee_fields.attendee_field_function"
                            ).id,
                        ],
                    )
                ]
            }
        )

        # create Portal User
        self.user_portal1 = self.env.ref("portal_event_tickets.user_portal1")

        sale_order, self.ticket1 = self._create_ticket(
            ticket_type=self.ticket_type_1,
            partner=self.user_portal1.partner_id,
            event=self.event,
        )
        sale_order.action_confirm()
        self.ticket1.confirm_registration()

        self.user_portal2 = self.env.ref("portal_event_tickets.user_portal2")

    def _create_ticket(self, ticket_type, partner, event):
        product = ticket_type.product_id

        # I create a sale order
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "note": "Invoice after delivery",
                "payment_term_id": self.env.ref("account.account_payment_term").id,
            }
        )

        # In the sale order I add some sale order lines. i choose event product
        sale_order_line = self.env["sale.order.line"].create(
            {
                "product_id": product.id,
                "price_unit": 190.50,
                "product_uom": self.env.ref("uom.product_uom_unit").id,
                "product_uom_qty": 1.0,
                "order_id": sale_order.id,
                "name": "sale order line",
                "event_id": event.id,
            }
        )

        # In the event registration I add some attendee detail lines. i choose event product
        register_person = self.env["registration.editor"].create(
            {
                "sale_order_id": sale_order.id,
                "event_registration_ids": [
                    (
                        0,
                        0,
                        {
                            "event_id": event.id,
                            "name": partner.name,
                            "email": partner.email,
                            "sale_order_line_id": sale_order_line.id,
                        },
                    )
                ],
            }
        )

        # I click apply to create attendees
        register_person.action_make_registration()

        return (
            sale_order,
            self.env["event.registration"].search([("origin", "=", sale_order.name)]),
        )
