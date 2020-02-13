from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    passport = fields.Char(
        string="Passport Number",
        compute=lambda s: s._compute_identification("passport", "passport",),
        inverse=lambda s: s._inverse_identification("passport", "passport",),
        search=lambda s, *a: s._search_identification("passport", *a),
    )
