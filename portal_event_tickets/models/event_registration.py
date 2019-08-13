# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# Copyright 2018 Ruslan Ronzhin <https://it-projects.info/team/rusllan/>
# Copyright 2019 Artem Rafailov <https://it-projects.info/team/Ommo73/>
# License MIT (https://opensource.org/licenses/MIT).-->
from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    # New fields
    is_transferring = fields.Boolean(
        "Ticket in transferring",
        help="Ticket transferring is started, but not finished",
        default=False,
    )
    was_transferred = fields.Boolean(
        "Ticket was transferred", help="Ticket was transferred", default=False,
    )
    origin_registration = fields.Many2one(
        "event.registration",
        compute="_compute_origin_registration",
        store=True,
        string="Original Ticket",
        track_visibility="onchange",
    )
    was_updated = fields.Boolean(
        "Ticket was updated",
        compute="_compute_was_updated",
        help="Ticket was transferred or updated",
        default=False,
    )

    # Updated fields
    email = fields.Char(track_visibility="onchange")
    phone = fields.Char(track_visibility="onchange")
    name = fields.Char(track_visibility="onchange")

    attendee_partner_id = fields.Many2one(track_visibility="onchange")
    partner_id = fields.Many2one(track_visibility="onchange")
    event_id = fields.Many2one(track_visibility="onchange")
    event_ticket_id = fields.Many2one(track_visibility="onchange")

    @api.multi
    @api.depends("sale_order_id", "sale_order_id.order_line")
    def _compute_origin_registration(self):
        for r in self:
            order = False
            if r.sale_order_id:
                refunded_lines = r.sale_order_id.order_line.filtered(
                    lambda l: l.refund_source_line_id
                ).mapped("refund_source_line_id")
                if refunded_lines:
                    order = refunded_lines[0].order_id
            r.origin_registration = order and self.search(
                [("state", "=", "cancel"), ("sale_order_id", "=", order.id)], limit=1
            )

    @api.multi
    @api.depends("was_transferred", "origin_registration")
    def _compute_was_updated(self):
        for r in self:
            r.was_updated = False
            if r.was_transferred or r.origin_registration:
                r.was_updated = True

    @api.multi
    def transferring_started(self, receiver):
        self.ensure_one()
        self.write(
            {
                "attendee_partner_id": receiver.id,
                "email": receiver.email,
                "name": receiver.name,
                "phone": receiver.phone,
                "is_transferring": True,
            }
        )

        # trigger email sending
        onsubscribe_schedulers = self.event_id.event_mail_ids.filtered(
            lambda s: s.interval_type == "transferring_started"
        )
        onsubscribe_schedulers.execute(self)  # self is a registration

    @api.multi
    def transferring_finished(self):
        self.ensure_one()
        receiver = self.attendee_partner_id
        # Update name and phone in registration, because those may be changed
        # Mark that transferring is finished
        self.write(
            {
                "name": receiver.name,
                "phone": receiver.phone,
                "is_transferring": False,
                "was_transferred": True,
            }
        )
        # trigger email sending
        onsubscribe_schedulers = self.event_id.event_mail_ids.filtered(
            lambda s: s.interval_type == "transferring_finished"
        )
        onsubscribe_schedulers.execute(self)  # self is a registration
