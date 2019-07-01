# -*- coding: utf-8 -*-
# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import SUPERUSER_ID
from odoo import http
from odoo.addons.website_blog.controllers.main import WebsiteBlog
from odoo.http import request


class WebsiteBlogExtended(WebsiteBlog):

    @http.route()
    def blog(self, blog=None, tag=None, page=1, **opt):
        blog_super = super(WebsiteBlogExtended, self).blog(blog, tag, page, **opt)

        if request.env.context.get('uid', 0) == SUPERUSER_ID:
            blog_env = blog_super.qcontext['blogs']
            updated_blogs = blog_env.search(request.env.ref('website_multi_company_blog.blog_rule_all').domain)
            blog_super.qcontext.update({
                'blogs': updated_blogs,
            })
        return blog_super
