from odoo import models, fields


class WebsiteTheme(models.Model):
    _inherit = 'website.theme'

    name = fields.Char(string="Theme")
    converted_theme_addon = fields.Char(
        string="Theme's technical name",
        help="")
