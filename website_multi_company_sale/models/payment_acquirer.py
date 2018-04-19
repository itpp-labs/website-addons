# coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    website_ids = fields.Many2many('website', string='Allowed websites',
                                   help='Set the websites this payment acquirer should be available on. Leave empty to allow all.')

    @api.onchange('company_id')
    def _onchange_company_id(self):
        return self.company_id and {'domain': {'website_ids': [('company_id', '=', self.company_id.id)]}} or {'domain': {'website_ids': []}}

    @api.constrains('company_id', 'website_ids')
    def _check_websites_in_company(self):
        for record in self:
            website_company = record.website_ids.mapped('company_id')
            if record.company_id and record.website_ids and (len(website_company) > 1 or website_company[0] != record.company_id):
                raise ValidationError(_("Error! Only the company's websites are allowed"))
