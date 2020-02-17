# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import api, fields, models, tools
from odoo.http import request

from odoo.addons.website_sale.models.website import Website as WebsiteOriginal


class Website(models.Model):
    _inherit = "website"

    billing_country_ids = fields.Many2many(
        "res.country",
        string="Billing Countries",
        help="Keep empty to allow all Countries",
    )

    @api.model
    @tools.ormcache_context(
        "self.env.uid",
        "country_code",
        "show_visible",
        "website_pl",
        "current_pl",
        "all_pl",
        "partner_pl",
        "order_pl",
        keys=("website_id",),
    )
    def _get_pl_partner_order(
        self,
        country_code,
        show_visible,
        website_pl,
        current_pl,
        all_pl,
        partner_pl=False,
        order_pl=False,
    ):
        """The extension can be removed once a branch has following update: https://github.com/odoo/odoo/pull/26414"""
        # call undecorated super method. See odoo/tools/cache.py::ormcache and http://decorator.readthedocs.io/en/stable/tests.documentation.html#getting-the-source-code
        return WebsiteOriginal._get_pl_partner_order.__wrapped__(
            self,
            country_code,
            show_visible,
            website_pl,
            current_pl,
            all_pl,
            partner_pl=partner_pl,
            order_pl=order_pl,
        )

    @api.multi
    def sale_get_order(
        self,
        force_create=False,
        code=None,
        update_pricelist=False,
        force_pricelist=False,
    ):
        company = request.website.company_id
        if not request.session.get("sale_order_id"):
            # original sale_get_order uses last_website_so_id only when there is no
            # sale_order_id in the session

            # company.id seems to be the same as self.id, but let's use variant
            # from original sale_get_order
            self = self.with_context(force_company=company.id)
        sale_order = super(Website, self).sale_get_order(
            force_create, code, update_pricelist, force_pricelist
        )

        if sale_order and force_create:
            sale_order.website_id = self.id

        return sale_order
