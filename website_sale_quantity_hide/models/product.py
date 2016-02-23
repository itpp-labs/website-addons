from openerp import api, models, fields

from openerp.tools import html_escape as escape
import werkzeug


class product_template(models.Model):
    _inherit = 'product.template'

    select_quantity = fields.Boolean('Select quantity',
                                     help='Allows select quantity in web shop',
                                     default=True)

    sale_one_only = fields.Boolean('Sale max 1 item',  help='Makes impossible to add more than one item to cart',
                                          default=False)

    @api.onchange('select_quantity')
    def onchange_select_quantity(self):
        self.ensure_one()
        if self.select_quantity:
            self.sale_one_only = False
