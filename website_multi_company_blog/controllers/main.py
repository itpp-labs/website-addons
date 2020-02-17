# -*- coding: utf-8 -*-
# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import SUPERUSER_ID, http
from odoo.http import request

from odoo.addons.website_blog.controllers.main import WebsiteBlog


class WebsiteBlogExtended(WebsiteBlog):
    @http.route()
    def blog(self, blog=None, tag=None, page=1, **opt):
        blog_super = super(WebsiteBlogExtended, self).blog(blog, tag, page, **opt)

        if request.env.context.get("uid", 0) == SUPERUSER_ID:
            blog_env = blog_super.qcontext["blogs"]
            updated_blogs = blog_env.search(
                request.env.ref("website_multi_company_blog.blog_rule_all").domain
            )
            blog_super.qcontext.update({"blogs": updated_blogs})
        return blog_super

    @http.route()
    def blogs(self, page=1, **post):
        blog_super = super(WebsiteBlogExtended, self).blogs(page, **post)

        if request.env.context.get("uid", 0) == SUPERUSER_ID:
            post_env = blog_super.qcontext["posts"]
            updated_posts = post_env.search(
                request.env.ref("website_multi_company_blog.post_rule_all").domain
            )
            blog_super.qcontext.update({"posts": updated_posts})
        return blog_super
