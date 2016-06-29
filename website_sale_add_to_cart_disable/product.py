from openerp import api, models, fields, SUPERUSER_ID


class product_template(models.Model):
    _inherit = 'product.template'

    sale_on_website = fields.Boolean('Show Add To Cart button', help='Switch off to disable sales via eCommerce', default=True)
