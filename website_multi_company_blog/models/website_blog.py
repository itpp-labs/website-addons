# -*- coding: utf-8 -*-

from odoo import models, fields


class Blog(models.Model):
    _inherit = 'blog.blog'

    website_ids = fields.Many2many('website', string='Allowed websites')
