# -*- coding: utf-8 -*-
import re
import urlparse

from odoo import models, SUPERUSER_ID, api

WEBSITE_REFS = [
    'website_multi_company_demo.website_books',
    'website_multi_company_demo.website_bikes',
    'website_multi_company_demo.website_watches',
]
WEBSITE_RE = r'shop\.(.*)\.example'


class Users(models.Model):
    _inherit = "res.users"

    @classmethod
    def authenticate(cls, db, login, password, user_agent_env):
        """ Update domain for websites by adding key name after first subdomain, for example:
        if base_location is "http://db123456.demo.it-projects.info/",
        then we replace "shop.SOMETHING.example"
        to "db123456.SOMETHING.demo.it-projects.info"
        """
        uid = super(Users, cls).authenticate(db, login, password, user_agent_env)
        with cls.pool.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            base_location = user_agent_env and user_agent_env.get('base_location')
            if not base_location:
                # Workaround for demo system based on https://it-projects-llc.github.io/odoo-saas-tools/
                #
                # "Saas Demo" creates templates with installed modules and then creates copies of that template.
                # So, we shall not make updates inside templates, but only inside final database
                return uid

            base = env['ir.config_parameter'].get_param('web.base.url') or base_location

            prefix = None
            suffix = None
            if base:
                domain = urlparse.urlsplit(base).netloc.split(':')[0]
                prefix, _, suffix = domain.partition('.')

            if not (prefix and suffix):
                return uid

            for wref in WEBSITE_REFS:
                website = env.ref(wref, raise_if_not_found=False)
                if not website:
                    continue
                m = re.search(WEBSITE_RE, website.domain)
                if not m:
                    continue
                key = m.group(1)
                website.domain = '{prefix}.{key}.{suffix}'.format(prefix=prefix, suffix=suffix, key=key)

        return uid
