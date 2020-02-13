from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    website_id = fields.Many2one("website", "Online Order Website", readonly=True)
