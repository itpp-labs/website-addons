from openerp import api, models, fields


class product_template(models.Model):
    _inherit = 'product.template'

    limit_per_order = fields.Integer('Limit per order')
    private_sale = fields.Boolean('Private Sale', default=False)
    private_sale_partner_ids = fields.Many2many('res.partner', 'product_private_sale_partner_rel', 'template_id', 
        'partner_id', string='Private Sale Partners')

    @api.model
    def _product_available(self):
        res = super(product_template, self)._product_available()
        print context
        print '++'*100
        return res


class res_partner(models.Model):
    _inherit = 'res.partner'

    private_sale_product_ids = fields.Many2many('product.template', 'product_private_sale_partner_rel', 'partner_id', 
        'template_id', string='Private Sale Products')
