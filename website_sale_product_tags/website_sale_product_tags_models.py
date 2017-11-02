from odoo import api
from odoo import fields
from odoo import models


class ProductTag(models.Model):
    _inherit = "product.template.tag"

    @api.model
    def _get_styles(self):
        return [
            ('label-default', 'Default (gray)'),
            ('label-primary', 'Primary (blue)'),
            ('label-success', 'Success (green)'),
            ('label-info', 'Info (light-blue)'),
            ('label-warning', 'Warning (orange)'),
            ('label-danger', 'Danger (red)'),

        ]

    style = fields.Selection(_get_styles, 'Style', help='Bootstrap class name to use on website. Default style is "primary".')
