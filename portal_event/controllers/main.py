# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request

from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.website_event.controllers.main import WebsiteEventController


class PortalEvent(website_account, WebsiteEventController):

    def _tickets_domain(self, partner=None):
        partner = partner or request.env.user.partner_id
        return [
            ('attendee_partner_id', '=', partner.id),
        ]

    @http.route()
    def account(self, **kw):
        """ Add sales documents to main account page """
        response = super(PortalEvent, self).account(**kw)

        domain = self._tickets_domain()
        tickets_count = request.env['event.registration'].search_count(domain)

        response.qcontext.update({
            'tickets_count': tickets_count,
        })
        return response

    @http.route(['/my/tickets', '/my/tickets/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_tickets(self, page=1, date_begin=None, date_end=None, **kw):
        values = self._prepare_portal_layout_values()
        Registration = request.env['event.registration']

        domain = self._tickets_domain()
        archive_groups = self._get_archive_groups('event.registration', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        ticket_count = Registration.search_count(domain)
        # make pager
        pager = request.website.pager(
            url="/my/tickets",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=ticket_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        tickets = Registration.search(domain, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'date': date_begin,
            'tickets': tickets,
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/tickets',
        })
        return request.render("portal_event.portal_my_tickets", values)

    @http.route(['/my/tickets/<int:ticket>'], type='http', auth="user", website=True)
    def ticket_page(self, ticket=None, **kw):
        values = self._prepare_portal_layout_values()
        ticket = request.env['event.registration'].browse([ticket])
        if not ticket or not ticket.exists():
            return request.render("website.404")

        has_access = True
        try:
            ticket.check_access_rights('read')
            ticket.check_access_rule('read')
        except AccessError:
            has_access = False

        has_access = has_access \
            or ticket.attendee_partner_id.id == request.env.user.partner_id \
            or request.env.user.has_group('event.group_event_manager')

        if not has_access:
            return request.render("website.403")

        ticket_sudo = ticket.sudo()

        values.update({
            'ticket': ticket_sudo,
        })
        return request.render("portal_event.portal_ticket_page", values)

    @http.route(['/my/tickets/transfer'], type='http', auth="user", methods=['GET'], website=True)
    def ticket_transfer_editor(self, **kw):
        """Special controller to customize result messages"""
        if not request.env.user.has_group('website.group_website_designer'):
            return request.render("website.403")

        values = self._prepare_portal_layout_values()
        values.update({
            'editor_mode': True,
            'error': kw.get('error')
        })
        return request.render("portal_event.portal_ticket_transfer", values)

    @http.route(['/my/tickets/transfer'], type='http', auth="user", methods=['POST'], website=True)
    def ticket_transfer(self, to_email, ticket_id, **kw):
        values = self._prepare_portal_layout_values()
        ticket = request.env['event.registration'].browse([int(ticket_id)])
        ticket.ensure_one()

        has_access = True
        try:
            ticket.check_access_rights('read')
            ticket.check_access_rule('read')
        except AccessError:
            has_access = False

        has_access = has_access \
            or ticket.attendee_partner_id.id == request.env.user.partner_id

        if not has_access:
            return request.render("website.403")

        error = None

        # Yes, error is None here but let's have correct indent for possible adding conditions.
        if not error:
            receiver = request.env['res.partner'].sudo().search([
                ('email', '=ilike', to_email)
            ], limit=1)

        if not receiver:
            error = 'receiver_not_found'

        if not error:
            domain = [('attendee_partner_id', '=', receiver.id),
                      ('state', 'not in', ['cancel']),
                      ('event_id', '=', ticket.event_id.id)]
            if request.env['event.registration'].search_count(domain):
                error = 'receiver_has_ticket'

        if not error:
            # do the transfer
            ticket.sudo().transferring_started(receiver)

        values.update({
            'to_email': to_email,
            'error': error,
        })
        return request.render("portal_event.portal_ticket_transfer", values)

    @http.route(['/my/tickets/transfer/receive'], type='http', auth="user", methods=['GET', 'POST'], website=True)
    def ticket_transfer_receive(self, transfer_ticket, **kw):
        ticket = transfer_ticket
        ticket = request.env['event.registration'].browse([int(ticket)])
        ticket.ensure_one()

        has_access = True
        try:
            ticket.check_access_rights('read')
            ticket.check_access_rule('read')
        except AccessError:
            has_access = False

        has_access = has_access \
            and ticket.attendee_partner_id.id == request.env.user.partner_id.id

        if not has_access or not ticket.is_transferring:
            return request.render("website.403")

        values = self._prepare_portal_layout_values()
        if request.httprequest.method == 'GET':
            tickets = self._process_tickets_details({'nb_register-0': 1})
            values.update({
                'transfer_ticket': ticket,
                'tickets': tickets,
                'event': ticket.event_id,
            })
            return request.env['ir.ui.view'].render_template(
                "portal_event.portal_ticket_transfer_receive", values)

        # handle filled form

        receiver = ticket.attendee_partner_id
        registration = self._process_registration_details(kw)[0]
        registration['event_id'] = ticket.event_id.id
        partner_vals = request.env['event.registration']._prepare_partner(registration)
        assert not partner_vals.get('email')

        receiver.sudo().write(partner_vals)

        ticket.sudo().transferring_finished()
        return request.redirect('/my/tickets')
