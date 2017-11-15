# -*- coding: utf-8 -*-
import logging

from odoo import models, api


_logger = logging.getLogger(__name__)


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model
    def _prepare_attendee_values(self, registration):
        """Extend it to pass partner values too (we remove them later in _prepare_partner)
        we skip partner_id field to avoid email field overriding. T
        """
        data = super(EventRegistration, self)._prepare_attendee_values(registration)
        partner_fields = self.env['res.partner']._fields
        data.update({key: registration[key] for key in registration.keys() if key in partner_fields and key != 'partner_id'})
        _logger.debug('_prepare_attendee_values: %s', data)
        return data

    def _prepare_partner(self, vals):
        """method from partner_event module"""
        event = self.env['event.event'].browse(vals['event_id'])
        if not event.attendee_field_ids:
            # attendee_field_ids is not configure
            # May happen in tests of other modules, which don't suppose that this module is installed.
            # Just return super values.
            return super(EventRegistration, self)._prepare_partner(vals)

        # copy partner fields to return and removes non-registration fields from vals
        res = {}
        partner_fields = self.env['res.partner']._fields
        _logger.debug('registration vals before removing: %s', vals)
        for field in event.attendee_field_ids:
            fn = field.field_name
            if field.field_model == 'res.partner' or fn in partner_fields:
                # partner fields
                value = vals.get(field.field_name)
                if value:
                    # Don't pass empty value, because it removes previous value.
                    # E.g. when partner with email is specified and known fields are not filled at the form
                    res[fn] = value

            if fn not in self._fields:
                # non-registration fields
                if fn in vals:
                    del vals[fn]

        _logger.debug('registration vals after removing: %s', vals)
        _logger.debug('partner values: %s', res)
        return res
