import logging

from odoo import http, _
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.fields import Date

from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.models.website import slug


_logger = logging.getLogger(__name__)


class PortalEvent(website_account):

    def _get_archive_groups(self, model, domain=None, fields=None, groupby="create_date", order="create_date desc"):
        # TODO make without copy-pasting. Probably add ir.rule for portal user?
        if not model:
            return []
        if domain is None:
            domain = []
        if fields is None:
            fields = ['name', 'create_date']
        groups = []
        for group in request.env[model].sudo()._read_group_raw(domain, fields=fields, groupby=groupby, orderby=order):
            dates, label = group[groupby]
            date_begin, date_end = dates.split('/')
            groups.append({
                'date_begin': Date.to_string(Date.from_string(date_begin)),
                'date_end': Date.to_string(Date.from_string(date_end)),
                'name': label,
                'item_count': group[groupby + '_count']
            })
        return groups

    def _tickets_domain(self, partner=None):
        partner = partner or request.env.user.partner_id
        return [
            ('attendee_partner_id', '=', partner.id),
            ('state', '=', 'open'),
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
        Registration = request.env['event.registration'].sudo()

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
        return request.render("portal_event_tickets.portal_my_tickets", values)

    def _has_ticket_access(self, ticket, to_update=False):
        """Ticket must not be sudo`ed"""
        env = ticket.env
        if not ticket.exists():
            _logger.info("ticket doesn't exist: %s", ticket)
            return False

        try:
            # We check only ir.rule records, because ir.model.access actually
            # doesn't allow portal user to read
            ticket.check_access_rule('read')
        except AccessError:
            groups = env.user.groups_id.mapped('name')
            _logger.info("Ticket access rights check is not passed! User groups: %s", groups, exc_info=True)
            return False

        if ticket.sudo().attendee_partner_id.id == ticket.env.user.partner_id.id:
            return True

        if to_update:
            _logger.info("No an attendee %s cannot update ticket %s, which belongs to %s",
                         ticket.env.user.partner_id,
                         ticket,
                         ticket.attendee_partner_id)
            # not an attendee, so cannot update
            return False

        return env.user.has_group('event.group_event_manager')

    @http.route(['/my/tickets/<int:ticket>'], type='http', auth="user", website=True)
    def ticket_page(self, ticket=None, **kw):
        values = self._prepare_portal_layout_values()
        ticket = request.env['event.registration'].browse(ticket)
        if not ticket or not ticket.exists():
            return request.render("website.404")

        if not self._has_ticket_access(ticket):
            return request.render("website.403")

        ticket_sudo = ticket.sudo()

        values.update({
            'ticket': ticket_sudo,
        })
        return request.render("portal_event_tickets.portal_ticket_page", values)

    @http.route(['/my/tickets/pdf/<int:ticket_id>'], type='http', auth="user", website=True)
    def portal_get_ticket(self, ticket_id=None, **kw):
        ticket = request.env['event.registration'].browse(ticket_id)

        if not self._has_ticket_access(ticket):
            return request.render("website.403")

        pdf = request.env['report'].sudo().get_pdf([ticket.id], 'event.event_registration_report_template_badge')
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
            ('Content-Disposition', 'attachment; filename=ticket.pdf;')
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)

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
        return request.render("portal_event_tickets.portal_ticket_transfer", values)

    @http.route(['/my/tickets/transfer'], type='http', auth="user", methods=['POST'], website=True)
    def ticket_transfer(self, to_email, ticket_id, **kw):
        values = self._prepare_portal_layout_values()

        error = self._ticket_transfer(request.env, to_email, ticket_id)

        values.update({
            'to_email': to_email,
            'error': error,
        })
        return request.render("portal_event_tickets.portal_ticket_transfer", values)

    def _ticket_transfer(self, env, to_email, ticket_id):
        """env is passed explicitly to use this method in ci tests"""
        ticket = env['event.registration'].browse(int(ticket_id))
        ticket.ensure_one()

        if not self._has_ticket_access(ticket, to_update=True):
            return request.render("website.403")

        ticket = ticket.sudo()

        if not ticket.event_id.ticket_transferring:
            return request.render("website.403")

        error = None

        # Yes, error is None here but let's have correct indent for possible adding conditions.
        if not error:
            receiver = env['res.partner'].sudo().search([
                ('email', '=ilike', to_email)
            ], limit=1)

        if not receiver:
            error = 'receiver_not_found'

        if not error:
            domain = [('attendee_partner_id', '=', receiver.id),
                      ('state', 'not in', ['cancel']),
                      ('event_id', '=', ticket.event_id.id)]
            if env['event.registration'].sudo().search_count(domain):
                error = 'receiver_has_ticket'

        if not error:
            # do the transfer
            ticket.transferring_started(receiver)

        return error

    @http.route(['/my/tickets/transfer/receive'], type='http', auth="user", methods=['GET', 'POST'], website=True)
    def ticket_transfer_receive(self, transfer_ticket=None, **kw):
        if transfer_ticket:
            ticket = request.env['event.registration'].browse(int(transfer_ticket))
        else:
            # Just take first available ticket. Mostly for unittests
            # Use sudo as portal user doesn't have access
            ticket = request.env['event.registration'].sudo().search([
                ('attendee_partner_id', '=', request.env.user.partner_id.id),
                ('is_transferring', '=', True),
            ], limit=1)
            # sudo back to original user
            ticket = ticket.sudo(request.env.user)

        ticket.ensure_one()

        if not self._has_ticket_access(ticket, to_update=True):
            return request.render("website.403")

        # we can make sudo once access is checked
        ticket = ticket.sudo()

        if not ticket.event_id.ticket_transferring:
            return request.render("website.403")

        values = self._prepare_portal_layout_values()
        if request.httprequest.method == 'GET':
            tickets = WebsiteEventController()._process_tickets_details({'nb_register-0': 1})
            values.update({
                'transfer_ticket': ticket,
                'tickets': tickets,
                'event': ticket.event_id,
            })
            return request.env['ir.ui.view'].render_template(
                "portal_event_tickets.portal_ticket_transfer_receive", values)

        # handle filled form

        receiver = ticket.attendee_partner_id
        registration = WebsiteEventController()._process_registration_details(kw)[0]
        registration['event_id'] = ticket.event_id.id
        partner_vals = request.env['event.registration']._prepare_partner(registration)
        assert not partner_vals.get('email')

        receiver.sudo().write(partner_vals)

        ticket.sudo().transferring_finished()
        return request.redirect('/my/tickets')

    @http.route(['/my/tickets/change'], type='http', auth="user", methods=['POST'], website=True)
    def ticket_change(self, ticket_id, **kw):
        ticket = request.env['event.registration'].browse(int(ticket_id))

        if not self._has_ticket_access(ticket, to_update=True):
            return request.render("website.403")

        if not ticket.event_id.ticket_changing:
            return request.render("website.403")

        ticket = ticket.sudo()
        line = ticket.sale_order_line_id
        assert line
        product = line.product_id

        order = request.website.sale_get_order(force_create=True)
        name = _('Ticket change: %s') % product.name
        order.add_refund_line(line, name, 1)

        # TODO: make redirection customizable
        return request.redirect("/event/%s/register" % slug(ticket.event_id))


class WebsiteSaleExtended(WebsiteSale):
    @http.route()
    def cart(self, **post):
        response = super(WebsiteSaleExtended, self).cart(**post)
        if post.get('total_is_negative'):
            response.qcontext.update({
                'warning_msg': _('Total amount is negative. Please add more tickets or products'),
            })
        return response
