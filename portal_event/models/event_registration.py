# -*- coding: utf-8 -*-
from odoo import models, fields


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    # New fields
    is_transferring = fields.Boolean('Ticket in transferring', help='Ticket transferring is started, but not finished')

    # Updated fields
    email = fields.Char(track_visibility='onchange')
    phone = fields.Char(track_visibility='onchange')
    name = fields.Char(track_visibility='onchange')

    attendee_partner_id = fields.Many2one(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    event_id = fields.Many2one(track_visibility='onchange')
    event_ticket_id = fields.Many2one(track_visibility='onchange')
