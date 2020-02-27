# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import SUPERUSER_ID, http
from odoo.http import request
from odoo.tools.safe_eval import safe_eval

from odoo.addons.website_blog.controllers.main import WebsiteBlog


# we use this hack
# after domain field in ir.rule was removed
# https://github.com/odoo/odoo/commit/172a767e5f7add9c5e806e00e0146dc5f09e806b#diff-e487de633a7ef116c20a824d203973a3
def get_domain_from_rule(rule):
    return safe_eval(rule.domain_force, rule._eval_context())


class WebsiteBlogExtended(WebsiteBlog):
    @http.route()
    def blog(self, blog=None, tag=None, page=1, **opt):
        blog_super = super(WebsiteBlogExtended, self).blog(blog, tag, page, **opt)

        if request.env.context.get("uid", 0) == SUPERUSER_ID:
            blog_env = blog_super.qcontext["blogs"]
            updated_blogs = blog_env.search(
                get_domain_from_rule(
                    request.env.ref("website_multi_company_blog.blog_rule_all")
                )
            )
            blog_super.qcontext.update({"blogs": updated_blogs})
        return blog_super

    @http.route()
    def blogs(self, page=1, **post):
        blog_super = super(WebsiteBlogExtended, self).blogs(page, **post)

        if request.env.context.get("uid", 0) == SUPERUSER_ID:
            post_env = blog_super.qcontext["posts"]
            updated_posts = post_env.search(
                get_domain_from_rule(
                    request.env.ref("website_multi_company_blog.post_rule_all")
                )
            )
            blog_super.qcontext.update({"posts": updated_posts})
        return blog_super
