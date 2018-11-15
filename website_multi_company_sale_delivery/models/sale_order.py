# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_delivery_methods(self):
        available_carriers = super(SaleOrder, self)._get_delivery_methods()
        delivery_access_user = self.env.ref('website_multi_company_sale_delivery.delivery_carrier_read_user')
        available_carriers = self.env['delivery.carrier'].sudo(delivery_access_user).search([('id', 'in', available_carriers.ids)]).sudo()
        return available_carriers
