# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    website_ids = fields.Many2many(
        "website",
        string="Allowed websites",
        help="Set the websites this delivery carrier should be available on. Leave empty to allow all.",
    )
