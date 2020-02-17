# Copyright 2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import api, models


class Menu(models.Model):
    _inherit = "website.menu"

    @api.onchange("website_id")
    def on_website_change(self):
        if self.parent_id and self.parent_id.website_id != self.website_id:
            self.parent_id = False
