from openerp import api, models, fields

from openerp.tools import html_escape as escape
import werkzeug


class product_template(models.Model):
    _inherit = 'product.template'

    sale_button = fields.Selection([
        ('add_to_cart', 'Add to cart'),
        ('buy_now', 'Buy now'),
        ('all', 'Add to cart & Buy now'),
    ], string='Sale button', help='''Type of sale in web shop.\n
After clicking on "buy now" at web shop:\n
* cart is cleared and the product is added\n
* user is redirected to /shop/checkout page\n
* page /shop/cart is still availabe, but\n
  * it doesn't have "continue shopping button"\n''',
                                   default='add_to_cart')
