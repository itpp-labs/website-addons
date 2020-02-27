# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models
from odoo.http import request


class ResCountry(models.Model):
    _inherit = "res.country"

    def get_website_sale_countries(self, mode="billing"):
        res = super(ResCountry, self).get_website_sale_countries(mode=mode)
        if mode == "billing" and request.website.billing_country_ids:
            res &= request.website.billing_country_ids
        return res
