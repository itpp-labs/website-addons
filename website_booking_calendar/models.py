# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import pytz

from odoo import api, models, fields
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

from odoo.addons.resource.resource import seconds

MIN_TIMESLOT_HOURS = 1
MIN_RESERVATION_MINUTES = 15


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def get_booking_available_products(self, event, products):
        return products

    @api.model
    def events_to_bookings(self, events):
        resource_obj = self.env['resource.resource']
        lang_obj = self.env['res.lang']
        lang = lang_obj.search([('code', '=', self.env.context.get('lang'))])
        user_df = ('%s %s' % (lang.date_format, lang.time_format)) if lang else DTF
        products = self.env['product.product'].search([('calendar_id', '!=', False),
                                                       ('website_published', '=', True)])
        bookings = {}
        partner = self.env.user.partner_id
        pricelist_id = partner.property_product_pricelist.id
        for event in events:
            r = event['resource']
            if r not in bookings:
                bookings[r] = {}
            start_dt = datetime.strptime(event['start'], DTF)
            end_dt = datetime.strptime(event['end'], DTF)
            # check products and its working calendars by every hour booked by user
            hour_dt = start_dt
            while hour_dt < end_dt:
                hour = hour_dt.strftime(DTF)
                if hour_dt < end_dt:
                    bookings[r][hour] = {
                        'start': hour_dt,
                        'start_f': (hour_dt).strftime(user_df),
                        'end': (hour_dt + timedelta(hours=MIN_TIMESLOT_HOURS)),
                        'end_f': (hour_dt + timedelta(hours=MIN_TIMESLOT_HOURS)).strftime(user_df),
                        'resource': resource_obj.browse(int(event['resource'])),
                        'products': {}
                    }
                    hour_end_dt = hour_dt + timedelta(hours=MIN_TIMESLOT_HOURS)
                    duration = seconds(hour_end_dt - hour_dt) / 3600
                    for product in self.get_booking_available_products(event, products):
                        hours = product.calendar_id.get_working_accurate_hours(hour_dt, hour_end_dt)
                        if hours >= duration:
                            bookings[r][hour]['products'][str(product.id)] = {
                                'id': product.id,
                                'name': product.name,
                                'quantity': 1,
                                'currency': product.company_id.currency_id.name
                            }
                    # join adjacent hour intervals to one SO position
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
                                bookings[r][h]['products'][id]['quantity'] += bookings[r][hour]['products'][id]['quantity']
                            del bookings[r][hour]
                            break
                hour_dt += timedelta(hours=MIN_TIMESLOT_HOURS)
        # calculate prices according to pricelists
        for k1, v1 in bookings.iteritems():
            for k2, v2 in v1.iteritems():
                for id, product in v2['products'].iteritems():
                    bookings[k1][k2]['products'][id]['price'] = self.env['product.product'].browse(product['id']).with_context({
                        'quantity': product['quantity'],
                        'pricelist': pricelist_id,
                        'partner': partner.id
                    }).price * product['quantity']
        res = []
        for r in bookings.values():
            res += r.values()
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _add_booking_line(self, product_id, resource, start, end, tz_offset=0):
        set_qty = 1
        for rec in self:
            if start and end:
                if not rec.env.context.get('tz'):
                    start = datetime.strptime(start, DTF) + timedelta(minutes=tz_offset)
                    end = datetime.strptime(end, DTF) + timedelta(minutes=tz_offset)
                else:
                    user_tz = pytz.timezone(rec.env.context.get('tz') or 'UTC')
                    start = user_tz.localize(fields.Datetime.from_string(start)).astimezone(pytz.utc)
                    end = user_tz.localize(fields.Datetime.from_string(end)).astimezone(pytz.utc)
                set_qty = (end - start).seconds / 3600
            values = self.sudo()._website_product_id_change(rec.id, product_id, qty=set_qty)
            values.update({
                'product_uom_qty': set_qty,
                'resource_id': int(resource),
                'booking_start': start,
                'booking_end': end,
            })
            if not self.env['sale.order.line'].sudo().is_overlaps(int(resource), start.strftime(DTF), end.strftime(DTF)):
                line = rec.env['sale.order.line'].sudo().with_context(tz_offset=tz_offset).create(values)
            else:
                line = None
        return line

    @api.model
    def _remove_unpaid_bookings(self):
        for order in self.search([('state', '=', 'draft')]):
            if order.section_id and order.section_id.code == 'WS':
                if fields.Datetime.from_string(order.date_order) \
                        + timedelta(minutes=MIN_RESERVATION_MINUTES) < datetime.now():
                    order.action_cancel()
