from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    website_id = fields.Many2one('website', 'Online Order Website', readonly=True)
