# Copyright 2017 Artyom Losev
# Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License MIT (https://opensource.org/licenses/MIT).
# Copyright 2020 Eugene Molotov <https://it-projects.info/team/em230418>

import logging

from odoo import models, tools

_logger = logging.getLogger(__name__)


class WebsiteCategoryCache(models.Model):

    _inherit = "website"

    @tools.cache("current_cat", "collapsed")
    def category_cache(
        self, current_cat, cats, slug, keep, parent_category_ids, collapsed=False
    ):
        if collapsed:
            template = "website_sale_cache.categories_collapsed_cache_template"
        else:
            template = "website_sale_cache.categories_cache_template"
        _logger.info("Product public categories were cached.")
        return self.env["ir.ui.view"].render_template(
            template,
            {
                "category": current_cat,
                "categories": cats,
                "slug": slug,
                "keep": keep,
                "parent_category_ids": parent_category_ids,
            },
        )

    def action_update_cache(self):
        _logger.info("Cache has been cleared.")
        return self.category_cache.clear_cache(self)
