# -*- coding: utf-8 -*-
from odoo import models


class Product(models.Model):
    _inherit = 'product.template'

    def _extend_domain(self, domain, context):
        if not (context and context.get('search_tags')):
            return domain
        domain = (['|', ('tag_ids', 'ilike', context.get('search_tags'))] +
                  domain)
        return domain

    def search_count(self, domain):
        domain = self._extend_domain(domain, context)
        return super(Product, self).search_count(
            cr, uid, domain)

    def search(self, domain, offset=0, limit=None, order=None,
               context=None, count=False):
        domain = self._extend_domain(domain, context)
        return super(Product, self).search(
            cr, uid, domain, offset=offset, limit=limit,
            order=order, count=count
        )
