from openerp import api, models, fields, SUPERUSER_ID


class product_template(models.Model):
    _name = 'product.template'
    _inherit = ['product.template', 'website_seo_url']

    seo_url = fields.Char('SEO URL', translate=True, index=True)
