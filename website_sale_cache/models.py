# -*- coding: utf-8 -*-
from openerp import models
from openerp import tools
import logging

_logger = logging.getLogger(__name__)


class WebsiteCategoryCache(models.Model):

    _inherit = 'website'

    @tools.cache()
    def category_cache(self, cats, slug, keep):
        _logger.info('Product public categories were cached.')
        return self._render('website_sale_cache.categories_cache_template', {'categories': cats,
                                                                             'slug': slug,
                                                                             'keep': keep})

    def action_update_cache(self):
        _logger.info('Cache has been cleared')
        return self.category_cache.clear_cache(self)
