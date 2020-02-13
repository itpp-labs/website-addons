from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    attendee_signup = fields.Boolean(
        string="Signup attendees to portal",
        help="Every attendee receives email to confirm email and set password to access to portal",
        default=False,
    )
