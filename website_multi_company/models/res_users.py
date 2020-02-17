# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = "res.users"

    editor_website_ids = fields.Many2many(
        "website",
        string="Editor on websites",
        help="Empty list allows edit any website",
    )

    @api.model
    def _get_company(self):
        """Try to get company from website first. It affects many models and feature,
        because it's used in _company_default_get which is used to compute
        default values on many models
        """
        # TODO this extention is moved to web_website (11.0), so it can be removed here
        website_id = self.env.context.get("website_id")
        if website_id:
            return self.env["website"].browse(website_id).company_id
        return super(ResUsers, self)._get_company()

    @api.onchange("company_ids")
    def _onchange_company_ids(self):
        return (
            self.company_ids
            and {
                "domain": {
                    "editor_website_ids": [("company_id", "in", self.company_ids.ids)]
                }
            }
            or {"domain": {"editor_website_ids": []}}
        )

    @api.constrains("company_ids", "editor_website_ids")
    def _check_websites_in_companies(self):
        for record in self:
            websites_companies = record.editor_website_ids.mapped("company_id")
            if (
                record.company_ids
                and record.editor_website_ids
                and not websites_companies <= record.company_ids
            ):
                raise ValidationError(
                    _(
                        "Error! You can select as editable only the allowed companies's websites - check the 'Editor on websites' field in preferences"
                    )
                )

    @api.multi
    def switch_multi_company(self, company):
        """
        :returns: True if company value was changed, otherwise False -- no access to change, None -- no need to change
        """
        self.ensure_one()

        user = self
        if user.company_id == company:
            return None

        update_company = True
        if company in user.company_ids:
            pass
        elif user.has_group("base.group_user"):
            # User is internal and doesn't have access to that company
            update_company = False
        else:
            # User is a portal user -- update his allowed companies
            user.write({"company_ids": [(4, company.id, 0)]})

        if update_company:
            user.company_id = company

        return update_company
