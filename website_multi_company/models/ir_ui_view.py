# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import logging

from odoo import _, exceptions, models

_logger = logging.getLogger(__name__)


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def make_multi_website(self):
        self.ensure_one()
        default_theme = self.env.ref(
            "website_multi_theme.theme_default", raise_if_not_found=False
        )
        if not default_theme:
            raise exceptions.UserError(
                _(
                    "Oops, Something is wrong: Default theme is not found. Try to update module website_multi_theme"
                )
            )

        all_websites = self.env["website"].search([])
        websites_without_theme = all_websites.filtered(lambda w: not w.multi_theme_id)
        if websites_without_theme:
            names = websites_without_theme.mapped("name")
            raise exceptions.UserError(
                _(
                    "Following Websites don't have Multi Theme: %s\n You need to update them first"
                )
                % ", ".join(names)
            )

        # not optimal way to search, but it's a problem for few websites adn themes
        all_themes = all_websites.mapped("multi_theme_id")
        themes_without_default_theme = all_themes.filtered(
            lambda theme: default_theme not in theme.upstream_dependencies()
        )
        if themes_without_default_theme:
            names = themes_without_default_theme.mapped("name")
            raise exceptions.UserError(
                _(
                    "Following multi-themes don't have Default Theme as Sub-Theme: %s\n You need to update them first"
                )
                % ", ".join(names)
            )

        Asset = self.env["website.theme.asset"]
        Asset.create({"name": self.xml_id, "theme_id": default_theme.id})
        self.env["res.config.settings"].multi_theme_reload()
        return True
