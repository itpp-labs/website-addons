# -*- coding: utf-8 -*-

from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request

from odoo.addons.website_portal.controllers.main import website_account


class website_account(website_account):

    def _tickets_domain(self, partner=None):
        partner = partner or request.env.user.partner_id
        return [
            ('partner_id', '=', partner.id),
        ]

    @http.route()
    def account(self, **kw):
        """ Add sales documents to main account page """
        response = super(website_account, self).account(**kw)

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
        ticket = request.env['event.registration'].browse([ticket])
        if not ticket:
            return request.render("website.404")

        has_access = True
        try:
            ticket.check_access_rights('read')
            ticket.check_access_rule('read')
        except AccessError:
            has_access = False

        has_access = has_access \
            or ticket.partner_id.id == request.env.user.partner_id \
            or request.env.user.has_group('event.group_event_manager')

        if not has_access:
            return request.render("website.403")

        ticket_sudo = ticket.sudo()

        return request.render("portal_event.portal_ticket_page", {
            'ticket': ticket_sudo,
        })
