# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models, api, tools
from odoo.addons.website_sale.models.website import Website as WebsiteOriginal


class Website(models.Model):
    _inherit = "website"

    @api.model
    @tools.ormcache_context('self.env.uid', 'country_code', 'show_visible', 'website_pl', 'current_pl', 'all_pl', 'partner_pl', 'order_pl', keys=("website_id",))
    def _get_pl_partner_order(self, country_code, show_visible, website_pl, current_pl, all_pl, partner_pl=False, order_pl=False):
        """The extension can be removed once a branch has following update: https://github.com/odoo/odoo/pull/26414"""
        # call undecorated super method. See odoo/tools/cache.py::ormcache and http://decorator.readthedocs.io/en/stable/tests.documentation.html#getting-the-source-code
        return WebsiteOriginal._get_pl_partner_order.__wrapped__(self, country_code, show_visible, website_pl, current_pl, all_pl, partner_pl=partner_pl, order_pl=order_pl)
