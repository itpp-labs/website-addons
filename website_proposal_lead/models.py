# -*- coding: utf-8 -*-
from odoo import models, fields
import re


def _get_proposal_id(self, name, args):
    res = {}
    for r in self.browse(ids):
        proposal_id = self.env['website_proposal.proposal'].search([('res_id', '=', r.id), ('res_model', '=', self._name)])
        res[r.id] = proposal_id and proposal_id[0]
        return res


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    _columns = {
        'proposal_template_id': fields.many2one('website_proposal.template', 'Proposal template'),
        'proposal_id': fields.function(_get_proposal_id, type='many2one', obj='website_proposal.proposal', string='Proposal'),
    }

    def create_proposal(self):
        for r in self.read(ids, ['proposal_template_id']):
            self.env['website_proposal.template'].create_proposal(r['proposal_template_id'][0], r['id'])
        return True

    def open_proposal(self):
        r = self.browse(ids[0], context)
        return self.env['website_proposal.proposal'].open_proposal([r.proposal_id.id])


class CrmMakeSale(models.TransientModel):
    _inherit = "crm.make.sale"

    def makeOrder(self):
        res = super(CrmMakeSale, self).makeOrder(ids, context)
        res_id = res['res_id']
        if not isinstance(res_id, list):
            res_id = [res_id]
        for order in self.env['sale.order'].read(res_id, ['id', 'origin']):
            lead_id = re.search(r'([0-9]+)', order['origin'])
            lead_id = lead_id and lead_id.group(0)
            if not lead_id:
                continue
            lead_id = int(lead_id)
            lead = self.env['crm.lead'].read([lead_id], ['proposal_id', 'proposal_template_id'])
            lead = lead and lead[0]
            if not lead:
                continue
            self.env['sale.order'].write([order['id']], {
                'proposal_id': lead.get('proposal_id') and lead.get('proposal_id')[0],
                'proposal_template_id': lead.get('proposal_template_id') and lead.get('proposal_template_id')[0],
            })
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _columns = {
        'proposal_template_id': fields.many2one('website_proposal.template', 'Proposal template'),
        'proposal_id': fields.many2one('website_proposal.proposal', 'Proposal'),
    }

    def create_proposal(self):
        ctx = (context and context.copy() or {})
        ctx['force_res_model'] = 'sale.order'
        for r in self.read(ids, ['proposal_template_id']):
            proposal_id = self.env['website_proposal.template'].create_proposal(r['proposal_template_id'][0], r['id'])
            self.write([r['id']], {'proposal_id': proposal_id})
        return True

    def open_proposal(self):
        r = self.browse(ids[0], context)
        return self.env['website_proposal.proposal'].open_proposal([r.proposal_id.id])
