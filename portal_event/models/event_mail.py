# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, tools, api


_INTERVALS = {
    'hours': lambda interval: relativedelta(hours=interval),
    'days': lambda interval: relativedelta(days=interval),
    'weeks': lambda interval: relativedelta(days=7*interval),
    'months': lambda interval: relativedelta(months=interval),
    'now': lambda interval: relativedelta(hours=0),
}


class EventMailScheduler(models.Model):

    _inherit = 'event.mail'

    interval_type = fields.Selection(selection_add=[
        ('transferring_started', 'Transferring started'),
        ('transferring_finished', 'Transferring finished'),
    ])

    @api.one
    @api.depends('event_id.state', 'event_id.date_begin', 'interval_type', 'interval_unit', 'interval_nbr')
    def _compute_scheduled_date(self):
        if self.interval_type not in ['transferring_started', 'transferring_finished']:
            return super(EventMailScheduler, self)._compute_scheduled_date()

        if self.event_id.state not in ['confirm', 'done']:
            self.scheduled_date = False
        else:
            date, sign = self.event_id.create_date, 1
            self.scheduled_date = datetime.strptime(date, tools.DEFAULT_SERVER_DATETIME_FORMAT) + _INTERVALS[self.interval_unit](sign * self.interval_nbr)


    @api.one
    def execute(self, registration=None):
        if self.interval_type not in ['transferring_started', 'transferring_finished']:
            return super(EventMailScheduler, self).execute()
        assert registration
        self.write({'mail_registration_ids': [
            (0, 0, {'registration_id': registration.id})
        ]})
        # execute scheduler on registrations
        self.mail_registration_ids.filtered(lambda reg: reg.scheduled_date and reg.scheduled_date <= datetime.strftime(fields.datetime.now(), tools.DEFAULT_SERVER_DATETIME_FORMAT)).execute()
        return True


class EventMailRegistration(models.Model):
    _inherit = 'event.mail.registration'

    @api.one
    @api.depends('registration_id', 'scheduler_id.interval_unit', 'scheduler_id.interval_type')
    def _compute_scheduled_date(self):
        if self.scheduler_id.interval_type not in ['transferring_started', 'transferring_finished']:
            return super(EventMailRegistration, self).execute()

        if self.registration_id:
            # date_open is not corresponded to its meaining,
            # but keep because it's copy-pasted code
            date_open_datetime = fields.datetime.now()
            self.scheduled_date = date_open_datetime + _INTERVALS[self.scheduler_id.interval_unit](self.scheduler_id.interval_nbr)
