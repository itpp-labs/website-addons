from odoo import models, api
from odoo.addons.website.models.website import slugify


class SEOURL(models.AbstractModel):
    _name = 'website_seo_url'

    _seo_url_field = 'seo_url'

    @api.model
    def _check_seo_url(self, vals, record_id=0):
        field = self._seo_url_field
        vals = vals or {}
        value = vals.get(field)
        if value:
            vals[field] = value = slugify(value)
            res = self.search([(field, '=', value), ('id', '!=', record_id)])
            if res:
                vals[field] = '%s-%s' % (vals[field], record_id)
        return vals

    @api.model
    def create(self, vals):
        vals = self._check_seo_url(vals)
        return super(SEOURL, self).create(vals)

    @api.multi
    def write(self, vals):
        for r in self:
            vals = r._check_seo_url(vals, record_id=r.id)
            super(SEOURL, r).write(vals)
        return True

    @api.multi
    def __check_seo_url_uniq(self):
        for r in self:
            value = getattr(r.with_context(lang=self.env.user.lang), self._seo_url_field)
            if value and len(self.with_context(lang=self.env.user.lang).search([(self._seo_url_field, '=', value)])) > 1:
                return False
        return True

    _constraints = [
        (__check_seo_url_uniq, 'SEO URL must be unique! Auto changing name failed. Try different name.', ['eq_seo_name']),
    ]
