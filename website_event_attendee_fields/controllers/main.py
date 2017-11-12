# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request


class Controller(http.Controller):

    @http.route(['/website_event_attendee_fields/check_email'], type='json', auth="public", methods=['POST'], website=True)
    def check_email(self, event_id, email):
        partner = request.env['res.partner'].sudo().search([
            ('email', '=', email),
        ], limit=1)
        if not partner:
            return {}

        registration = request.env['event.registration'].sudo().search([
            ('event_id', '=', event_id),
            ('partner_id', '=', partner.id),
            ('state', '=', 'open'),
        ])
        if registration:
            return {
                'email_not_allowed': _('This email address is already signed up for the event')
            }

        event = request.env['event.event'].sudo().browse(event_id)
        known_fields = []
        for f in event.attendee_field_ids:
            if f.field_name == 'email':
                continue
            if getattr(partner, f.field_name):
                known_fields.append(f.field_name)

        return {
            'known_fields': known_fields
        }



