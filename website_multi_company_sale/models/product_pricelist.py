# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
import logging

from odoo import _, api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    def _default_website(self):
        return self.env["website"].search(
            [
                "|",
                ("company_id", "=", self.env.user.company_id.id),
                ("company_id", "=", False),
            ],
            order="company_id DESC",
            limit=1,
        )

    @api.onchange("company_id")
    def _onchange_company_id(self):
        return (
            self.company_id
            and {"domain": {"website_id": [("company_id", "=", self.company_id.id)]}}
            or {"domain": {"website_id": []}}
        )

    @api.constrains("company_id", "website_id")
    def _check_websites_in_company(self):
        for record in self:
            website_company = record.website_id.company_id
            if record.company_id and website_company != record.company_id:
                raise ValidationError(
                    _(
                        "Error! Only the company's websites are allowed. \
                    Leave the Company field empty or select corresponding company"
                    )
                )

    def _get_partner_pricelist(self, partner_id, company_id=None):
        """Call with new context to extend domain in search method.
        Also, update company_id according to website value"""
        website_id = self.env.context.get("website_id")
        if website_id:
            self = self.with_context(search_pricelist_website=website_id)
            company_id = self.env["website"].sudo().browse(website_id).company_id.id
        return super(Pricelist, self)._get_partner_pricelist(
            partner_id, company_id=company_id
        )

    @api.model
    def search(self, domain, offset=0, limit=None, order=None, count=False):
        if self.env.context.get("search_pricelist_website"):
            # Add website to search domain

            # We don't need to add company, because default pricelist for a
            # company can be configured via ir.property.
            website_id = self.env.context["search_pricelist_website"]
            domain += [
                "|",
                ("website_id", "=", website_id),
                ("website_id", "=", False),
            ]
            order = "website_id DESC"
            limit = 1
            _logger.debug("Updated domain: %s", domain)

        res = super(Pricelist, self).search(
            domain, offset=offset, limit=limit, order=order, count=count
        )

        return res
