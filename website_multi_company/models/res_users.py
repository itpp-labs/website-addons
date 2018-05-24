from odoo import models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def switch_multi_company(self, company):
        """
        :returns: Is company set to new value
        """
        self.ensure_one()

        user = self
        if user.company_id == company:
            return True

        update_company = True
        if company in user.company_ids:
            pass
        elif user.has_group('base.group_user'):
            # User is internal and doesn't have access to that company
            update_company = False
        else:
            # User is a portal user -- update his allowed companies
            user.write({
                'company_ids': [(4, company.id, 0)]
            })

        if update_company:
            user.company_id = company

        return update_company
