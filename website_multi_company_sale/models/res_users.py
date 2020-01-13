# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create_new_portal_user_template(self, company_id):
        default_param = self.env['ir.config_parameter'].sudo().search([('key', '=', 'base.template_portal_user_id')])

        tmplt_user = self.browse(int(default_param.value or False)).sudo()
        new_template_user = tmplt_user.copy({
            'login': tmplt_user.name + ' for ' + company_id.name,
            'company_ids': [(6, 0, company_id.ids)],
            'company_id': company_id.id,
        })
        # update property values
        default_property = self.env['ir.property'].search([
            ('res_id', '=', 'ir.config_parameter,' + str(default_param.id)),
            ('company_id', '=', False)
        ], limit=1)
        new_property = default_property.sudo().copy({
            'company_id': company_id.id,
            'value_text': new_template_user.id,
        })
        return new_template_user, new_property
