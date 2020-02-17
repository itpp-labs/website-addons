# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models


class IrActionsActUrl(models.Model):
    _inherit = "ir.actions.act_url"

    def read(self, fields=None, load="_classic_read"):
        res = super(IrActionsActUrl, self).read(fields=fields, load=load)
        for data in res:
            if data["xml_id"] == "website.action_website":
                url = self._action_website_url(data)
                if url:
                    data["url"] = url
        return res

    def _action_website_url(self, data):
        website = self.env.user.backend_website_id
        if not website:
            website = self.env["website"].search(
                [("company_id", "=", self.env.user.company_id.id)]
            )
            if len(website) != 1:
                return False

        if website.domain in ["localhost", "0.0.0.0"] or website.domain.endswith(
            ".example"
        ):
            return False

        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("web.base.url", "")
            .startswith("https://")
        ):
            scheme = "https"
        else:
            scheme = "http"
        url = "{}://{}/".format(scheme, website.domain)
        return url
