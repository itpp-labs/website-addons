# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_delivery_methods(self):
        available_carriers = super(SaleOrder, self)._get_delivery_methods()
        public = self.env.ref('base.public_user')
        available_carriers = self.env['delivery.carrier'].sudo(public).search([('id', 'in', available_carriers.ids)]).sudo()
        return available_carriers
