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

