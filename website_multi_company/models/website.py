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

        # convert_assets and copy views for current website
        self._multi_theme_activate()

    @api.multi
    def multi_theme_reload_list(self):
        # only reloads list
        self.env["website.theme"].search([])._convert_assets()

    @api.multi
    def _multi_theme_activate(self):
        if not self.env.context.get('skip_converting_assets'):
            # reload dependencies before activating
            self.mapped('multi_theme_id')\
                .upstream_dependencies()\
                ._convert_assets()
        return super(Website, self)._multi_theme_activate()
