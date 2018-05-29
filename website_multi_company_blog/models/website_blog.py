
from odoo import models, fields


class Blog(models.Model):
    _inherit = 'blog.blog'

    website_ids = fields.Many2many('website', string='Allowed websites', help='Set the websites your blog should be available on. Leave empty to post the blog on each website you created.')
