# -*- coding: utf-8 -*-
from odoo import models, fields
import uuid
from odoo import tools, _


try:
    from odoo.addons.email_template.email_template import mako_template_env
except ImportError:
    try:
        from odoo.addons.mail.mail_template import mako_template_env
    except ImportError:
        pass


class WebsiteProposalTemplate(models.Model):
    _name = "website_proposal.template"
    _description = "Proposal Template"
    _columns = {
        'name': fields.char('Proposal Template', required=True),

        'head': fields.text('Html head'),
        'page_header': fields.html('Page header'),
        'website_description': fields.html('Description'),
        'page_footer': fields.html('Page footer'),

        'res_model': fields.char('Model', help="The database object this template will be applied to"),
    }

    def open_template(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/website_proposal/template/%d' % ids[0]
        }

    def create_proposal(self, template_id, res_id):
        if not template_id:
            return False
        if isinstance(template_id, list):
            template_id = template_id[0]

        template = self.env['website_proposal.template'].browse(template_id)

        vals = {'template_id': template_id,
                'head': template.head,
                'page_header': template.page_header,
                'website_description': template.website_description,
                'page_footer': template.page_footer,
                'res_id': res_id,
                'res_model': context.get('force_res_model') or template.res_model,
                }

        proposal_id = self.env['website_proposal.proposal'].create(vals, context)
        return proposal_id


class WebsiteProposal(models.Model):
    _name = 'website_proposal.proposal'
    _rec_name = 'id'

    def _get_default_company(self):
        company_id = self.env['res.users']._get_company(context=context)
        if not company_id:
            raise UserError(_('Error!'), _('There is no default company for the current user!'))
        return company_id

    def _get_res_name(self, name, args):
        res = {}
        for r in self.browse(ids):
            record = self.env[r.res_model].browse(r.res_id)
            res[r.id] = record.name
        return res

    _columns = {
        'res_name': fields.function(_get_res_name, string='Name', type='char'),
        'access_token': fields.char('Security Token', required=True, copy=False),
        'template_id': fields.many2one('website_proposal.template', 'Quote Template', readonly=True),
        'head': fields.text('Html head'),
        'page_header': fields.text('Page header'),
        'website_description': fields.html('Description'),
        'page_footer': fields.text('Page footer'),

        'res_model': fields.char('Model', readonly=True, help="The database object this is attached to"),
        'res_id': fields.integer('Resource ID', readonly=True, help="The record id this is attached to", select=True),
        'sign': fields.binary('Singature'),
        'sign_date': fields.datetime('Signing Date'),
        'signer': fields.binary('Signer'),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('rejected', 'Rejected'),
            ('done', 'Signed'),
        ]),
        'company_id': fields.many2one('res.company', 'Company'),
    }
    _defaults = {
        'access_token': lambda self, cr, uid, ctx={}: str(uuid.uuid4()),
        'company_id': _get_default_company,
        'state': 'draft',
    }

    def open_proposal(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/website_proposal/%s' % (ids[0])
        }

    def edit_proposal(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/website_proposal/%s?enable_editor' % (ids[0])
        }

    def create(self, vals):
        record = self.env[vals.get('res_model']).browse(vals.get('res_id'))

        mako = mako_template_env.from_string(tools.ustr(vals.get('website_description')))
        website_description = mako.render({'record': record})
        website_description = website_description.replace('template-only-', '')

        vals['website_description'] = website_description
        new_id = super(WebsiteProposal, self).create(vals)
        return new_id


class MailMessageSubtype(models.Model):
    _inherit = 'mail.message.subtype'
    _columns = {
        'internal': fields.boolean('Internal', help="don't publish these messages")
    }
    _defaults = {
        'internal': False
    }
