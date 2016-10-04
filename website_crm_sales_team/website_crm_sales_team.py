# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import SUPERUSER_ID


class CrmLead(osv.Model):
    _inherit = "crm.lead"

    def create(self, cr, uid, vals, context=None):

        channel_id = None
        try:
            channel_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'crm', 'crm_case_channel_website')[1]
        except ValueError:
            pass
        if channel_id is not None and \
            'channel_id' in vals and \
            channel_id == vals['channel_id'] and \
                'section_id' not in vals:
            section_ids = self.pool.get("crm.case.section").search(
                cr, SUPERUSER_ID, [("code", "=", "Website")], context=context)
            if section_ids:
                vals['section_id'] = section_ids[0]

        return super(CrmLead, self).create(cr, uid, vals, context=context)
