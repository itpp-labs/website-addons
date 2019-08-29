from odoo import models, api


class Product(models.Model):
    _inherit = 'product.template'

    def _extend_domain(self, domain):
        if (self.env.context.get('search_tags') and
                ('tag_ids', 'ilike', self.env.context.get('search_tags')) not in domain):

            # calculating position, after which domain new domains must be placed
            i = domain.index(('sale_ok', '=', True)) + 1
            while type(domain[i]) in [tuple, list] and i < len(domain):
                i = i + 1

            domain.insert(i, '|')
            domain.insert(i + 1, ('tag_ids', 'ilike', self.env.context.get('search_tags')))
        return domain

    @api.model
    def search_count(self, domain):
        domain = self._extend_domain(domain)
        return super(Product, self).search_count(domain)

    @api.model
    def search(self, domain, offset=0, limit=None, order=None, count=False):
        domain = self._extend_domain(domain)
        return super(Product, self).search(
            domain, offset=offset, limit=limit,
            order=order, count=count
        )
