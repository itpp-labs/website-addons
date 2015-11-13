import re
import simplejson

from openerp import http, SUPERUSER_ID
from openerp.http import request


class website_booking_calendar(http.Controller):

    def _get_resources(self, params):
        cr, uid, context = request.cr, request.uid, request.context
        resource_obj = request.registry['resource.resource']
        domain=[('to_calendar','=',True)]
        resource_ids = resource_obj.search(cr, SUPERUSER_ID, domain, context=context)
        resources = resource_obj.browse(cr, SUPERUSER_ID, resource_ids, context=context)
        return resources

    def _get_values(self, params):
        values = {
            'resources': self._get_resources(params)
        }
        return values

    def _get_template(self, params):
        return 'website_booking_calendar.index'


    @http.route(['/booking/calendar'], type='http', auth="public", website=True)
    def calendar(self, **kwargs):
        return request.website.render(self._get_template(kwargs), self._get_values(kwargs))

    @http.route('/booking/calendar/events', type='json', auth='public', website=True)
    def events(self, start, end, resources=[]):
        cr, uid, context = request.cr, request.uid, request.context
        return request.registry["sale.order.line"].get_bookings(cr, SUPERUSER_ID, start, end, resources, context=context)

    @http.route('/booking/calendar/events/add', type='json', auth='public', website=True)
    def add_event(self, start, resource_id, end=None):
        cr, uid, context = request.cr, request.uid, request.context
        return request.registry["sale.order.line"].add_backend_booking(cr, uid, resource_id, start, end, context=context)

    @http.route('/booking/calendar/confirm/form', type='http', auth='public', website=True)
    def confirm_form(self, **kwargs):
        events = simplejson.loads(kwargs['events'])
        cr, uid, context = request.cr, request.uid, request.context
        bookings = request.registry["sale.order.line"].events_to_bookings(cr, SUPERUSER_ID, events, context=context)
        return request.website.render('website_booking_calendar.confirm_form', {
            'bookings': bookings
        })

    @http.route('/booking/calendar/confirm', type='http', auth='public', website=True)
    def order(self, **kwargs):
        for key, arg in kwargs.iteritems():
            if key.startswith('product_id'):
                m = re.match('^product_id\[(\d+)\]\[([\d-]+ [\d:]+)\-([\d-]+ [\d:]+)\]$', key)
                resource_id = m.group(1)
                start = m.group(2)
                end = m.group(3)
                request.website.sale_get_order(force_create=1)._add_booking_line(int(arg), int(resource_id), start, end)
        return request.redirect("/shop/checkout")