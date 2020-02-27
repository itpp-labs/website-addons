# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import api, models


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def create(self, vals):
        result = super(ResCompany, self).create(vals)

        default_param = (
            self.env["ir.config_parameter"]
            .sudo()
            .search([("key", "=", "base.template_portal_user_id")])
        )
        if default_param.id == result.id:
            return result
        self.env["res.users"].create_new_portal_user_template(result)
        return result
