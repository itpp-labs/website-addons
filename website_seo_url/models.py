# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import _, api, models
from odoo.exceptions import ValidationError

from odoo.addons.website.models.website import slugify


class SEOURL(models.AbstractModel):
    _name = "website_seo_url"
    _description = "Website SEO URL"

    _seo_url_field = "seo_url"

    @api.model
    def _check_seo_url(self, vals, record_id=0):
        field = self._seo_url_field
        vals = vals or {}
        value = vals.get(field)
        if value:
            vals[field] = value = slugify(value)
            res = self.search([(field, "=", value), ("id", "!=", record_id)])
            if res:
                vals[field] = "{}-{}".format(vals[field], record_id)
        return vals

    @api.model
    def create(self, vals):
        vals = self._check_seo_url(vals)
        return super(SEOURL, self).create(vals)

    def write(self, vals):
        for r in self:
            vals = r._check_seo_url(vals, record_id=r.id)
            super(SEOURL, r).write(vals)
        return True

    @api.constrains("_seo_url_field")
    def _check_seo_url_uniq(self):
        for r in self:
            value = getattr(
                r.with_context(lang=self.env.user.lang), self._seo_url_field
            )
            if (
                value
                and len(
                    self.with_context(lang=self.env.user.lang).search(
                        [(self._seo_url_field, "=", value)]
                    )
                )
                > 1
            ):
                raise ValidationError(
                    _(
                        "SEO URL must be unique! Auto changing name failed. Try different name."
                    )
                )
