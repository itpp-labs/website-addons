from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    last_website_so_id = fields.Many2one(company_dependent=True, website_dependent=True)
