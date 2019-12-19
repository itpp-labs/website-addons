# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_billing_country_ids = fields.Many2many(related='website_id.billing_country_ids',
                                                   string='Billing Countries', readonly=False)

    @api.multi
    def open_template_user(self):
        current_user_company = self.env['res.users'].browse(self._context['uid']).company_id
        default_param = self.env['ir.config_parameter'].sudo().search([('key', '=', 'base.template_portal_user_id')])
        proper_property = self.env['ir.property'].search([
            ('res_id', '=', 'ir.config_parameter,' + str(default_param.id)),
            ('company_id', '=', current_user_company.id)
        ], limit=1)

        if not proper_property:
            self.env['res.users'].create_new_portal_user_template(current_user_company)
        return super(ResConfigSettings, self.with_context(force_company=current_user_company.id)).open_template_user()
