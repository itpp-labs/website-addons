# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.exceptions import UserError
from odoo.addons.base.module.module import ACTION_DICT
from odoo import api

BASE_MODULES = ['website', 'website_sale', 'website_blog', 'website_sale_comparison', 'website_sale_wishlist', 'mass_mailing', 'web_settings_dashboard']


class Module(models.Model):
    _inherit = "ir.module.module"

    def button_install(self):
        # domain to select auto-installable (but not yet installed) modules
        auto_domain = [('state', '=', 'uninstalled'), ('auto_install', '=', True)]

        # determine whether an auto-install module must be installed:
        #  - all its dependencies are installed or to be installed,
        #  - at least one dependency is 'to install'
        install_states = frozenset(('installed', 'to install', 'to upgrade'))

        def must_install(module):
            states = set(dep.state for dep in module.dependencies_id)
            return states <= install_states and 'to install' in states

        modules = self
        while modules:
            # Mark the given modules and their dependencies to be installed.
            modules.state_update('to install', ['uninstalled'])

            # Determine which auto-installable modules must be installed.
            modules = self.search(auto_domain).filtered(must_install)

        # retrieve the installed (or to be installed) theme modules
        theme_category = self.env.ref('base.module_category_theme')
        theme_modules = self.search([
            ('state', 'in', list(install_states)),
            ('category_id', 'child_of', [theme_category.id]),
        ])

        # determine all theme modules that mods depends on, including mods
        def theme_deps(mods):
            deps = mods.mapped('dependencies_id.depend_id')
            while deps:
                mods |= deps
                deps = deps.mapped('dependencies_id.depend_id')
            return mods & theme_modules

        # NEW STUFF: keep original code for easier maintenance, but block execution by adding "False and" to if block
        if False and any(module.state == 'to install' for module in theme_modules):
            # check: the installation is valid if all installed theme modules
            # correspond to one theme module and all its theme dependencies
            if not any(theme_deps(module) == theme_modules for module in theme_modules):
                state_labels = dict(self.fields_get(['state'])['state']['selection'])
                themes_list = [
                    "- %s (%s)" % (module.shortdesc, state_labels[module.state])
                    for module in theme_modules
                ]
                raise UserError(_(
                    "You are trying to install incompatible themes:\n%s\n\n"
                    "Please uninstall your current theme before installing another one.\n"
                    "Warning: switching themes may significantly alter the look of your current website pages!"
                ) % ("\n".join(themes_list)))
        return dict(ACTION_DICT, name=_('Install'))

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self.env.context.get('search_theme_dependencies'):
            args = args or []
            args += self._theme_dependencies_domain(self.env.context.get('search_theme_dependencies'))
        return super(Module, self)._search(args, offset, limit, order, count, access_rights_uid)

    @api.model
    def _theme_dependencies_domain(self, theme_name):
        """Computes domain for dependencies of the theme, but without built-in dependencies"""
        if not theme_name:
            return []

        self = self.with_context(search_theme_dependencies=False)

        theme = self.search([('name', '=', theme_name)])
        if not theme:
            return []

        deps = theme.upstream_dependencies(exclude_states=('to remove'))
        base_modules = self.search([('name', 'in', BASE_MODULES)])
        base_deps = base_modules.upstream_dependencies(exclude_states=('to remove'))
        deps -= base_modules
        deps -= base_deps

        return [('id', 'in', deps.ids)]
