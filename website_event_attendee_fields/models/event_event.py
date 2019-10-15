from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval


class Event(models.Model):
    _inherit = 'event.event'
    attendee_field_ids = fields.Many2many('event.event.attendee_field')
    use_attendees_header = fields.Boolean(compute='_compute_use_attendees_header')

    @api.multi
    def _compute_use_attendees_header(self):
        for r in self:
            total_width = sum([int(f.width) or 1 for f in self.attendee_field_ids])
            r.use_attendees_header = total_width <= 12

    @api.multi
    def check_partner_for_new_ticket(self, partner_id):
        if self.partner_is_participating(partner_id):
            return _('This email address is already signed up for the event')
        return None

    @api.multi
    def partner_is_participating(self, partner_id):
        self.ensure_one()
        registration = self.env['event.registration'].sudo().search([
            ('event_id', '=', self.id),
            ('partner_id', '=', partner_id),
            ('state', '=', 'open'),
        ])
        return registration


class AttendeeField(models.Model):

    _name = 'event.event.attendee_field'

    sequence = fields.Integer('Sequence')
    field_id = fields.Many2one('ir.model.fields', domain="[('model_id.model', 'in', ['res.partner', 'event.registration'])]")
    field_name = fields.Char(related='field_id.name', readonly=True)
    field_model = fields.Char(related='field_id.relation', readonly=True)
    field_description = fields.Char(related='field_id.field_description', readonly=True)
    is_required = fields.Boolean('Required', default=True)
    form_type = fields.Selection([
        ('color', 'Color'),
        ('date', 'Date'),
        ('datetime', 'Date and Time'),
        ('datetime-local', 'Date and Time (local)'),
        ('email', 'Email'),
        ('month', 'Month'),
        ('number', 'Number'),
        ('password', 'Password'),
        ('search', 'Search'),
        ('tel', 'Phone'),
        ('text', 'Text'),
        ('time', 'Time'),
        ('url', 'URL'),
        ('week', 'Week'),
        ('many2one', 'Many2one'),
    ], string='Type at Form', default='text', required=True)

    width = fields.Selection([
        (str(v), str(v))
        for v in xrange(1, 13)  # 13 is not included
    ], string='Width', required=True, default='4', help="Field of a width in the form. One row may have width up to 12")

    domain = fields.Char('Domain')

    @api.multi
    def name_get(self):
        return [
            (r.id, '#%s: %s (width=%s)' % (r.sequence, r.field_name, r.width, ))
            for r in self
        ]

    @api.multi
    def get_select_options(self):
        self.ensure_one()
        domain = safe_eval(self.domain or '[]')
        records = self.env[self.field_model].search(domain)
        res = [
            {
                'id': r.id,
                'name': r.display_name,
            }
            for r in records
        ]
        return res

    @api.multi
    def get_value(self, partner):
        self.ensure_one()
        v = getattr(partner, self.field_name)
        if self.form_type == 'many2one':
            v = v.id
        return v
