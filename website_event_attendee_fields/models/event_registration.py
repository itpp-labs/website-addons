# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
import logging

from odoo import _, api, models

_logger = logging.getLogger(__name__)


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model
    def create(self, vals):
        partner_exists = False
        if vals.get("email"):
            Partner = self.env["res.partner"]
            email = vals.get("email").replace("%", "").replace("_", "\\_")
            partner_exists = Partner.search([("email", "=ilike", email)], limit=1)

        res = super(EventRegistration, self).create(vals)

        if res.attendee_partner_id:
            # be sure, that name and phone in registration are ones from Attendee,
            # because built-in modules take them from Partner (buyer) if ones are no presented
            res.name = res.attendee_partner_id.name
            res.phone = res.attendee_partner_id.phone

            if partner_exists:
                partner_vals = self._prepare_partner(vals)
                # Update attendee details, if user buys (register) ticket for himself
                # self.env.user is Administrator here, so just trust to partner_id field
                if res.attendee_partner_id == res.partner_id:
                    res.attendee_partner_id.sudo().write(partner_vals)

                elif len(partner_vals) > 1:
                    # If vals has more than email address
                    # Add a note about posible problems with updating fields

                    # FIXME partner_vals always has more than one field (e.g. event_ticket_id, origin, etc).
                    # So, this message is always posted
                    res.message_post(
                        _(
                            "Attendee partner record are not updated for security reasons:<br/> %s "
                        )
                        % partner_vals
                    )

        return res

    @api.model
    def _prepare_attendee_values(self, registration):
        """Extend it to pass partner values too (we remove them later in _prepare_partner)
        we skip partner_id field to avoid email field overriding.
        """
        data = super(EventRegistration, self)._prepare_attendee_values(registration)
        partner_fields = self.env["res.partner"]._fields
        data.update(
            {
                key: registration[key]
                for key in registration.keys()
                if key in partner_fields and key != "partner_id"
            }
        )
        _logger.debug("_prepare_attendee_values: %s", data)
        return data

    def _prepare_partner(self, vals):
        """method from partner_event module"""
        event = self.env["event.event"].browse(vals["event_id"])
        if not event.attendee_field_ids:
            # attendee_field_ids is not configure
            # May happen in tests of other modules, which don't suppose that this module is installed.
            # Just return super values.
            return super(EventRegistration, self)._prepare_partner(vals)

        # copy partner fields to return and removes non-registration fields from vals
        res = {}
        partner_fields = self.env["res.partner"]._fields
        _logger.debug("registration vals before removing: %s", vals)
        for field in event.attendee_field_ids:
            fn = field.field_name
            if field.field_model == "res.partner" or fn in partner_fields:
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

        _logger.debug("registration vals after removing: %s", vals)
        _logger.debug("partner values: %s", res)
        return res
