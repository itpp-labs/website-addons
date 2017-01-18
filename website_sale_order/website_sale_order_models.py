# -*- coding: utf-8 -*-
from odoo import models
from odoo import fields as old_fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _columns = {
        'name': old_fields.char('Name', required=True, select=True, track_visibility='onchange'),
        'phone': old_fields.char('Phone', track_visibility='onchange'),
    }
