from openerp import api, models, fields, SUPERUSER_ID
from openerp.exceptions import ValidationError


class resource_resource(models.Model):
    _inherit = 'resource.resource'

    to_calendar = fields.Boolean('Display on calendar')


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'    

    resource_id = fields.Many2one('resource.resource', 'Resource')
    booking_start = fields.Datetime(string="Date start")
    booking_end = fields.Datetime(string="Date end")

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
        elif self.resource_id or self.booking_start or self.booking_end:
            raise ValidationError('Provide all of booking parameters')

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
            'start': b.booking_start,
            'end': b.booking_end,
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

