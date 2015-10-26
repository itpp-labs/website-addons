from datetime import datetime, timedelta
from dateutil import rrule
import pytz

from openerp import api, models, fields, SUPERUSER_ID
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from openerp.exceptions import ValidationError

MIN_TIMESLOT_HOURS = 1

class resource_resource(models.Model):
    _inherit = 'resource.resource'

    to_calendar = fields.Boolean('Display on calendar')


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'    

    resource_id = fields.Many2one('resource.resource', 'Resource')
    booking_start = fields.Datetime(string="Date start")
    booking_end = fields.Datetime(string="Date end")
    calendar_id = fields.Many2one('resource.calendar', related='product_id.calendar_id')

    @api.one
    @api.constrains('resource_id', 'booking_start', 'booking_end')
    def _check_date_overlap(self):
        if self.resource_id and self.booking_start and self.booking_end:
            overlaps = self.search_count(['&','|','&',('booking_start', '>', self.booking_start), ('booking_start', '<', self.booking_end),
                                          '&',('booking_end', '>', self.booking_start), ('booking_end', '<', self.booking_end),
                                          ('id', '!=', self.id),
                                          ('resource_id', '!=', False),
                                          ('resource_id', '=', self.resource_id.id)
            ])
            overlaps += self.search_count([('id', '!=', self.id),
                                           ('booking_start', '=', self.booking_start),
                                           ('booking_end', '=', self.booking_end),
                                           ('resource_id', '=', self.resource_id.id)])
            if overlaps:
                raise ValidationError('There already is booking at that time.')

    @api.multi
    @api.constrains('calendar_id', 'booking_start', 'booking_end')
    def _check_date_fit_product_calendar(self):
        for record in self:
            if record.calendar_id and record.booking_start and record.booking_end:
                is_valid = self.validate_time_limits(record.calendar_id.id, record.booking_start, record.booking_end)
                if not is_valid:
                    raise ValidationError('Not valid interval of booking for the product %s.' % self.product_id.name)

    @api.model
    def validate_time_limits(self, calendar_id, booking_start, booking_end):
        calendar_obj = self.env['resource.calendar']
        leave_obj = self.env['resource.calendar.leaves']
        user_tz = pytz.timezone(self.env.context.get('tz', 'UTC'))
        start_dt = pytz.utc.localize(fields.Datetime.from_string(booking_start)).astimezone(user_tz)
        end_dt = pytz.utc.localize(fields.Datetime.from_string(booking_end)).astimezone(user_tz)
        hours = calendar_obj.browse(calendar_id).get_working_hours(start_dt, end_dt)
        if not hours:
            return False
        else:
            hours = hours[0]
        duration = (end_dt - start_dt).seconds/3600
        if hours != duration:
            leaves = leave_obj.search([('name','=','PH'), ('calendar_id','=',calendar_id)])
            leave_intervals = []
            for l in leaves:
                leave_intervals.append((datetime.strptime(l.date_from, DTF),
                                        datetime.strptime(l.date_to, DTF)
                ))
            clean_intervals = calendar_obj.interval_remove_leaves((start_dt, end_dt), leave_intervals)
            hours += duration
            for interval in clean_intervals:
                hours -= (interval[1] - interval[0]).seconds/3600
            if hours != duration:
                return False
        return True

    @api.model
    def get_bookings(self, start, end, resource_ids):
        domain  = [
            ('booking_start', '>=', start), 
            ('booking_end', '<=', end),
            ('booking_start', '>=', fields.Datetime.now()),
            ]
        if resource_ids:
            domain.append(('resource_id', 'in', resource_ids))
        bookings = self.search(domain)
        return [{
            'id': b.id,
            'title': b.resource_id.name,
            'start': '%s+00:00' % b.booking_start,
            'end': '%s+00:00' % b.booking_end,
            'resourceId': b.resource_id.id,
            'editable': False,
        } for b in bookings]

    @api.model
    def add_backend_booking(self, resource_id, start, end):

        booking_id = self.create({
            'resource_id': resource_id,
            'booking_start': start,
            'booking_end': end, 
        })

        return booking_id.id

    @api.model
    def events_to_bookings(self, events):
        calendar_obj = self.env['resource.calendar']
        resource_obj = self.env['resource.resource']
        lang_obj = self.env['res.lang']
        lang = lang_obj.search([('code', '=', self.env.context.get('lang'))])
        user_df = ('%s %s' % (lang.date_format, lang.time_format)) if lang else DTF
        products = self.env['product.product'].search([('calendar_id','!=',False)])
        bookings = {}
        for event in events:
            r = event['resource']
            if not r in bookings:
                bookings[r] = {}
            start_dt = datetime.strptime(event['start'], DTF)
            end_dt = datetime.strptime(event['end'], DTF)
            #check products and its working calendars by every hour booked by user
            hour_dt = start_dt
            while hour_dt < end_dt:
                hour = hour_dt.strftime(DTF)
                if hour_dt < end_dt:
                    bookings[r][hour] = {
                        'start': hour_dt,
                        'start_f': (hour_dt).strftime(user_df),
                        'end': (hour_dt+timedelta(hours=MIN_TIMESLOT_HOURS)),
                        'end_f': (hour_dt+timedelta(hours=MIN_TIMESLOT_HOURS)).strftime(user_df),
                        'resource': resource_obj.browse(int(event['resource'])),
                        'products': {}
                    }
                    for product in products:
                        duration = product.calendar_id.get_working_hours(hour_dt, hour_dt+timedelta(hours=MIN_TIMESLOT_HOURS))
                        if duration and duration[0] == MIN_TIMESLOT_HOURS:
                            bookings[r][hour]['products'][str(product.id)] = {
                                'id': product.id,
                                'name': product.name,
                                'price': product.lst_price or product.price,
                                'currency': product.company_id.currency_id.name
                            }
                    #join adjacent hour intervals to one SO position
                    for h in bookings[r]:
                        if h == hour or bookings[r][h]['products'].keys() != bookings[r][hour]['products'].keys():
                            continue
                        adjacent = False
                        if bookings[r][hour]['start'] == bookings[r][h]['end']:
                            adjacent = True
                            bookings[r][h].update({
                                'end': bookings[r][hour]['end'],
                                'end_f': bookings[r][hour]['end_f']
                            })
                        elif bookings[r][hour]['end'] == bookings[r][h]['start']:
                            adjacent = True
                            bookings[r][h].update({
                                'start': bookings[r][hour]['end'],
                                'start_f': bookings[r][hour]['start_f']
                            })
                        if adjacent:
                            for id, p in bookings[r][h]['products'].iteritems():
                                bookings[r][h]['products'][id]['price'] += bookings[r][hour]['products'][id]['price']
                            del bookings[r][hour]
                            break
                hour_dt += timedelta(hours=MIN_TIMESLOT_HOURS)
        res = []
        for r in bookings.values():
            res += r.values()
        return res

class product_template(models.Model):
    _inherit = 'product.template'

    calendar_id = fields.Many2one('resource.calendar', string='Working time')


class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _add_booking_line(self, product_id, resource, start, end):
        set_qty = 1
        for rec in self:
            if start and end:
                user_tz = pytz.timezone(rec.env.context.get('tz', 'UTC'))
                start = user_tz.localize(fields.Datetime.from_string(start)).astimezone(pytz.utc)
                end = user_tz.localize(fields.Datetime.from_string(end)).astimezone(pytz.utc)
                set_qty = (end - start).seconds/3600
            values = self.sudo()._website_product_id_change(rec.id, product_id, qty=set_qty)
            values.update({
                'product_uom_qty': set_qty,
                'resource_id': int(resource),
                'booking_start': start,
                'booking_end': end,
            })
            line = rec.env['sale.order.line'].sudo().create(values)
        return line