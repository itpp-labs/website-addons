from datetime import datetime, timedelta
import pytz

from openerp import api, models, fields
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

from openerp.addons.resource.resource import seconds

MIN_TIMESLOT_HOURS = 1


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'  

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
                    hour_end_dt = hour_dt+timedelta(hours=MIN_TIMESLOT_HOURS)
                    duration = seconds(hour_end_dt - hour_dt)/3600
                    for product in products:
                        hours = product.calendar_id.get_working_accurate_hours(hour_dt, hour_end_dt)
                        if hours == duration:
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
