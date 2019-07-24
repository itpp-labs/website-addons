from odoo import http
from odoo.http import request
from odoo.addons.website_event.controllers.main import WebsiteEventController
import re


class WebsiteEventControllerExtended(WebsiteEventController):
    @http.route()
    def registration_confirm(self, event, **post):
        """Check that threre are no email duplicates.
        There is a check on frontend, but that is easy to get around."""
        registrations = self._process_registration_details(post)
        emails = [r.get("email", "").strip() for r in registrations]
        assert len(emails) == len(set(emails))
        res = super(WebsiteEventControllerExtended, self).registration_confirm(event, **post)
        if res.location:
            # If super redirect (to /shop/checkout)
            url = request.env['ir.config_parameter'].get_param('website_event_sale.redirection') or res.location
            return request.redirect(url)
        else:
            return res

    def _process_registration_details(self, details):
        """ Remove spaces in emails """
        res = super(WebsiteEventControllerExtended, self)._process_registration_details(details)
        for registration in res:
            if registration.get('email'):
                registration['email'] = registration.get('email').strip()
        return res

    @http.route(['/website_event_attendee_fields/check_email'], type='json', auth="public", methods=['POST'], website=True)
    def check_email(self, event_id, email):
        partner = request.env['res.partner'].sudo().search([
            ('email', '=', email),
        ], limit=1)
        if not partner:

            def remove_spaces(s):
                s = re.sub(r'^\s*', '', s)
                s = re.sub(r'\s*$', '', s)
                return s

            email = remove_spaces(email)
            partner = request.env['res.partner'].sudo().search([
                '|', '|',
                ('email', '=ilike', '% ' + email),
                ('email', '=ilike', '% ' + email + ' %'),
                ('email', '=ilike', email + ' %')
            ], limit=1)
            partner_email = remove_spaces(partner.email)
            if not partner:
                return {}
            # It's a workaround in order to prevent duplicating partner accounts when buying a ticket
            partner.write({
                'email': partner_email
            })

        event = request.env['event.event'].sudo().browse(event_id)
        error_msg = event.check_partner_for_new_ticket(partner.id)
        if error_msg:
            return {
                'email_not_allowed': error_msg
            }

        known_fields = []
        for f in event.attendee_field_ids:
            if f.field_name == 'email':
                continue
            if getattr(partner, f.field_name):
                known_fields.append(f.field_name)

        return {
            'known_fields': known_fields
        }
