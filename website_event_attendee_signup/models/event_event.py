# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    attendee_signup = fields.Boolean(string="Signup attendees to portal",
                                     help="Every attendee receives email to confirm email and set password to access to portal",
                                     default=False)
