from odoo import models, api, fields
from odoo.http import request


class Website(models.Model):
    _inherit = 'website'

    @api.multi
    def sale_get_order(self, force_create=False, code=None, update_pricelist=False, force_pricelist=False):
        company = request.website.company_id
        if not request.session.get('sale_order_id'):
            # original sale_get_order uses last_website_so_id only when there is
            # sale_order_id in the session

            # company.id seems to be the same as self.id, but let's use variant
            # from original sale_get_order
            self = self.with_context(force_company=company.id)
        return super(Website, self).sale_get_order(force_create, code, update_pricelist, force_pricelist)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    last_website_so_id = fields.Many2one(company_dependent=True)
