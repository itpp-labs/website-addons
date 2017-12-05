# -*- coding: utf-8 -*-
from odoo import models, fields, api


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    # New fields
    is_transferring = fields.Boolean(
        'Ticket in transferring',
        help='Ticket transferring is started, but not finished',
        default=False,
    )

    # Updated fields
    email = fields.Char(track_visibility='onchange')
    phone = fields.Char(track_visibility='onchange')
    name = fields.Char(track_visibility='onchange')

    attendee_partner_id = fields.Many2one(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    event_id = fields.Many2one(track_visibility='onchange')
    event_ticket_id = fields.Many2one(track_visibility='onchange')

    @api.multi
    def transferring_started(self, receiver):
        self.ensure_one()
        self.write({
            'attendee_partner_id': receiver.id,
            'email': receiver.email,
            'name': receiver.name,
            'phone': receiver.phone,
            'is_transferring': True,
        })

        # trigger email sending
        onsubscribe_schedulers = self.event_id.event_mail_ids.filtered(
            lambda s: s.interval_type == 'transferring_started')
        onsubscribe_schedulers.execute(self)  # self is a registration

    @api.multi
    def transferring_finished(self):
        self.ensure_one()
        receiver = self.attendee_partner_id
        # Update name and phone in registration, because those may be changed
        # Mark that transferring is finished
        self.write({
            'name': receiver.name,
            'phone': receiver.phone,
            'is_transferring': False,
        })
        # trigger email sending
        onsubscribe_schedulers = self.event_id.event_mail_ids.filtered(
            lambda s: s.interval_type == 'transferring_finished')
        onsubscribe_schedulers.execute(self)  # self is a registration

    @api.multi
    def confirm_registration(self):
        # FIXME: old tickets are not canceled and they are changed to products!
        res = super(EventRegistration, self).confirm_registration()
        order = self.sale_order_line_id.order_id
        refunded_lines = order.order_line.mapped('refund_source_line_id')
        self.search([('sale_order_line_id', 'in', refunded_lines.ids)]).button_reg_cancel()

        # post a message why it was canceled
        res.message_post_with_view(
            'portal_event.message_origin_link',
            values={'origin': order},
            subtype_id=self.env.ref('mail.mt_note').id)

        return res
