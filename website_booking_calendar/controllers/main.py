from openerp import http
from openerp.http import request


class website_booking_calendar(http.Controller):

    @http.route(['/booking/calendar'], type='http', auth="public", website=True)
    def calendar(self, order_line=None):
        cr, uid, context = request.cr, request.uid, request.context
        resource_obj = request.registry['resource.resource']

        resource_ids = resource_obj.search(cr, uid, [('to_calendar','=',True)], context=context)
        resources = resource_obj.browse(cr, uid, resource_ids, context=context)
        values = {
            'resources': resources,
        }
        return request.website.render("website_booking_calendar.index", values)

    @http.route('/booking/calendar/events', type='json', auth='public', website=True)
    def events(self, start, end):
        cr, uid, context = request.cr, request.uid, request.context
        return request.registry["resource.booking"].get_bookings(cr, uid, start, end, context=context)

    @http.route('/booking/calendar/events/add', type='json', auth='public', website=True)
    def add_event(self, start, resource_id, end=None, order_line=None):
        cr, uid, context = request.cr, request.uid, request.context
        return request.registry["resource.booking"].add_backend_booking(cr, uid, resource_id, start, end, order_line, context=context)

