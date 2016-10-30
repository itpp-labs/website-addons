# -*- coding: utf-8 -*-
import re
import simplejson

from openerp import http, SUPERUSER_ID
from openerp.http import request


class WebsiteBookingCalendar(http.Controller):

    def _get_resources(self, params):
        cr, context = request.cr, request.context
        resource_obj = request.registry['resource.resource']
        domain = [('to_calendar', '=', True)]
        resource_ids = resource_obj.search(cr, SUPERUSER_ID, domain, context=context)
        resources = resource_obj.browse(cr, SUPERUSER_ID, resource_ids, context=context)
        return resources

    def _get_values(self, params):
        values = {
            'resources': self._get_resources(params)
        }
        return values

    @http.route(['/booking/calendar'], type='http', auth="public", website=True)
    def calendar(self, **kwargs):
        return request.website.render('website_booking_calendar.index', self._get_values(kwargs))

    @http.route('/booking/calendar/confirm/form', type='http', auth='public', website=True)
    def confirm_form(self, **kwargs):
        events = simplejson.loads(kwargs['events'])
        cr, context = request.cr, request.context
        bookings = request.registry["sale.order.line"].events_to_bookings(cr, SUPERUSER_ID, events, context=context)
        return request.website.render('website_booking_calendar.confirm_form', {
            'bookings': bookings
        })

    @http.route('/booking/calendar/confirm', type='http', auth='public', website=True)
    def order(self, **kwargs):
        tz = int(kwargs.get('timezone', '0'))
        for key, arg in kwargs.iteritems():
            if key.startswith('product_id'):
                m = re.match(r'^product_id\[(\d+)\]\[([\d-]+ [\d:]+)\-([\d-]+ [\d:]+)\]$', key)
                resource_id = m.group(1)
                start = m.group(2)
                end = m.group(3)
                order = request.website.sale_get_order(force_create=1)
                if order.state in ['cancel', 'done']:
                    request.website.sale_reset()
                    order = request.website.sale_get_order(force_create=1)
                order._add_booking_line(int(arg), int(resource_id), start, end, tz)
        return request.redirect("/shop/cart")

    @http.route('/booking/calendar/slots', type='json', auth='public', website=True)
    def get_free_slots(self, **kwargs):
        cr, uid, context = request.cr, SUPERUSER_ID, request.context
        return request.registry["sale.order.line"].get_free_slots(cr, uid, kwargs.get('start'),
                                                                  kwargs.get('end'), kwargs.get('tz'), kwargs.get('domain', []), online=True, context=context)

    @http.route('/booking/calendar/slots/booked', type='json', auth='public', website=True)
    def get_booked_slots(self, **kwargs):
        cr, uid, context = request.cr, SUPERUSER_ID, request.context
        return request.registry["sale.order.line"].get_bookings(cr, uid, kwargs.get('start'),
                                                                kwargs.get('end'), kwargs.get('tz'), kwargs.get('domain', []), online=True, context=context)
