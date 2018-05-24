import logging

from odoo import models, api
from odoo.tools import pycompat

_logger = logging.getLogger(__name__)


class MailTemplate(models.Model):
    "Templates for sending email"
    _inherit = "mail.template"

    @api.model
    def render_template(self, template_txt, model, res_ids, post_process=False):
        """Add company_id to context to force use that company when
        get_param('web.base.url') is called in a method which replaces local links (links
        without hostname, e.g. '/my/orders/1')

        """
        company_id = self.env.context.get('company_id')
        if company_id:
            return super(MailTemplate, self).render_template(template_txt, model, res_ids, post_process=post_process)

        multi_mode = True
        if isinstance(res_ids, pycompat.integer_types):
            multi_mode = False
            res_ids = [res_ids]

        results = dict.fromkeys(res_ids, u"")

        records = self.env[model].browse(filter(None, res_ids))  # filter to avoid browsing [None]
        for r in records:
            if hasattr(r, 'company_id'):
                company_id = r.company_id.id
            else:
                # while ir_config_parameter_multi_company takes company_id
                # from user by default, it doesn't work if sudo is called
                # somewhere (especially it's important in odoo 11.0 where
                # you cannot use get_param without sudo)
                company_id = self.env.user.company_id.id
            new_self = self.with_context(company_id=company_id)
            res = super(MailTemplate, new_self).render_template(template_txt, model, r.id, post_process=post_process)
            results[r.id] = res

        return multi_mode and results or results[res_ids[0]]
