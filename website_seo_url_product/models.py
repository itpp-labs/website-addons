from odoo import fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "website_seo_url"]

    seo_url = fields.Char("SEO URL", translate=True, index=True)
