# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, api


BASE_MODULES = ['website_blog', 'website_sale_comparison', 'website_sale_wishlist', 'web_settings_dashboard', 'website_crm', 'website_animate', 'website_mass_mailing', 'contacts', 'fetchmail', 'resource', 'calendar', 'snippet_google_map']


class Module(models.Model):
    _inherit = "ir.module.module"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self.env.context.get('search_theme_dependencies'):
            args = args or []
            args += self._theme_dependencies_domain(self.env.context.get('search_theme_dependencies'))
        return super(Module, self)._search(args, offset, limit, order, count, access_rights_uid)

    @api.model
    def _search_theme_dependencies(self, theme_name):
        """Search dependencies of the theme, but without built-in dependencies"""
        if not theme_name:
            return self

        self = self.with_context(search_theme_dependencies=False)

        theme = self.search([('name', '=', theme_name)])
        if not theme:
            return self

        deps = theme.upstream_dependencies(exclude_states=('to remove'))
        base_modules = self.search([('name', 'in', BASE_MODULES)])
        base_deps = base_modules.upstream_dependencies(exclude_states=('to remove'))
        deps -= base_modules
        deps -= base_deps

        return self.search([('id', 'in', deps.ids)])
