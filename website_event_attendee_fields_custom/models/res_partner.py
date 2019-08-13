# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2019 Artem Rafailov <https://it-projects.info/team/Ommo73/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    passport = fields.Char(
        string="Passport Number",
        compute=lambda s: s._compute_identification("passport", "passport",),
        inverse=lambda s: s._inverse_identification("passport", "passport",),
        search=lambda s, *a: s._search_identification("passport", *a),
    )
