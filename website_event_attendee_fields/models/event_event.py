# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Event(models.Model):
    _inherit = 'event.event'
    attendee_fields = fields.Many2many('event.event.attendee_field')


class AttendeeField(models.Model):

    _name = 'event.event.attendee_field'

    field_id = fields.Many2one('ir.model.fields')
    field_name = fields.Char(related='field_id.name', readonly=True)
    field_description = fields.Char(related='field_id.field_description', readonly=True)
    is_required = fields.Boolean('Required', default=True)
    form_type = fields.Selection([
        ('text', 'Text'),
        ('tel', 'Phone'),
        ('email', 'Email'),
    ], string='Type at Form')

    width = fields.Selection([
        (str(v), str(v))
        for v in xrange(1, 13)  # 13 is not included
    ], string='Width', help="Field of a width in the form. One row may have width up to 12")

    @api.multi
    def name_get(self):
        return [
            (r.id, '%s (width=%s)' % (r.field_name, r.width))
            for r in self
        ]
