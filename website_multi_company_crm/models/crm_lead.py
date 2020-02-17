# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Lead(models.Model):
    _inherit = "crm.lead"

    def _default_website_id(self):
        return self.env.context.get("website_id") or self.env.user.backend_website_id.id

    website_id = fields.Many2one(
        "website", string="From Website", default=_default_website_id
    )
    company_id = fields.Many2one(
        default=lambda self: self.env["res.company"]._company_default_get()
    )

    @api.onchange("company_id")
    def _onchange_company_id(self):
        return (
            self.company_id
            and {"domain": {"website_id": [("company_id", "in", self.company_id.ids)]}}
            or {"domain": {"website_id": []}}
        )

    @api.constrains("company_id", "website_id")
    def _check_website_in_company(self):
        for record in self:
            if (
                record.company_id
                and record.website_id
                and not record.website_id.company_id == record.company_id
            ):
                raise ValidationError(_("Error! Website and Company are mismatched"))
