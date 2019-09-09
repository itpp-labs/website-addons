# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, api, tools, fields
from odoo.addons.website_sale.models.website import Website as WebsiteOriginal
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    order_duplicating = fields.Boolean(string='Automatic Order Duplicating',
                                       help='Duplicate orders for Daughter companies')
    order_duplicating_companies = fields.Many2many('res.company', string='Order Duplicating Companies',
                                                   help='Daughter companies where order is being automatically duplicated to')
