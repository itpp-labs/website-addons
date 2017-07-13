# -*- coding: utf-8 -*-
from odoo import models, api


class Menu(models.Model):
    _inherit = "website.menu"

    @api.onchange('website_id')
    def on_website_change(self):
        if self.parent_id and self.parent_id.website_id != self.website_id:
            self.parent_id = False
