# -*- coding: utf-8 -*-
# Copyright 2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import logging

from odoo import models, api

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"

    @api.multi
    def multi_theme_reload(self):
        self.ensure_one()

        # Find theme views
        self.multi_theme_id._convert_assets()

        # Update views for current website
        self._multi_theme_activate()

    @api.multi
    def multi_theme_reload_list(self):
        # only reloads list
        self.env["website.theme"].search([])._convert_assets()
