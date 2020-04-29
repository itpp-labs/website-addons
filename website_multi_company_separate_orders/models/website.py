# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    split_orders = fields.Boolean(
        string="Automatic Order Splitting", help="Split orders for Daughter companies"
    )
    split_orders_companies = fields.Many2many(
        "res.company",
        string="Order Duplicating Companies",
        help="Daughter companies where order is being automatically duplicated to",
    )

    @api.model
    def website_domain(self, website_id=False):
        res = super(Website, self).website_domain(website_id)
        website_id = website_id or self.get_current_website()
        if (
            not website_id
            or self.env.context
            and self.env.context.get("website_id", False)
        ):
            return res

        if type(website_id) == int:
            website_id = self.env["website"].browse(website_id)
        website_company_parent_id = website_id.sudo().company_id.sudo().parent_id
        if website_company_parent_id:
            child_websites = (
                self.env["website"]
                .search([("company_id", "=", website_company_parent_id.id)])
                .ids
            )
            upd_tuple = res[0][2] + tuple(child_websites)
            upd_res_0 = list(res[0])
            upd_res_0[2] = upd_tuple
            res[0] = tuple(upd_res_0)
        return res


# class Users(models.Model):
#     _inherit = 'res.users'
#
#     @classmethod
#     def _login(cls, db, login, password):
#         res = super(Users, cls)._login(db, login, password)
#         import wdb; wdb.set_trace()
#         return res
