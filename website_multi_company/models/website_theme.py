# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class WebsiteTheme(models.Model):
    _inherit = 'website.theme'

    name = fields.Char(string="Theme")
    converted_theme_addon = fields.Char(
        string="Theme's technical name",
        help="")

    @api.multi
    def _convert_assets(self):
        """Generate assets for converted themes"""
        for one in self:
            assets_before = one.asset_ids
            super(WebsiteTheme, one)._convert_assets()
            assets_after = one.asset_ids
            if not assets_before and assets_after:
                # new theme: update dependencies
                one.write(one._autofill_deps())

    @api.multi
    def _autofill_deps(self):
        self.ensure_one()
        modules = self\
            .env['ir.module.module']\
            ._search_theme_dependencies(
                self.converted_theme_addon
            ).mapped('name')

        existing_themes = self.search([
            ('converted_theme_addon', 'in', modules)
        ]).mapped('converted_theme_addon')
        new_themes = set(modules) - set(existing_themes)
        for converted_theme_addon in new_themes:
            self.create({
                'name': converted_theme_addon,
                'converted_theme_addon': converted_theme_addon,
            })
        themes = self.search([('converted_theme_addon', 'in', modules)])
        try:
            themes |= self.env.ref('website_multi_theme.theme_default')
        except:
            pass
        return {
            'dependency_ids': [(6, 0, themes.ids)],
        }

    @api.onchange('converted_theme_addon')
    def onchange_converted_theme_addon(self):
        self.update(self._autofill_deps())
