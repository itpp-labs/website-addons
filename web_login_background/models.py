# -*- coding: utf-8 -*-

from openerp import fields, api
from openerp import models


class IRAttachmentBackground(models.Model):
    _inherit = 'ir.attachment'

    use_as_background = fields.Boolean("Use as login page background", default=False)

    @api.multi
    def check(self, mode, values=None):
        ids = self.ids
        cr = self.env.cr
        if ids and mode == 'read':
            if isinstance(ids, (int, long)):
                ids = [ids]
            ids = ids[:]  # make a copy
            cr.execute('SELECT id,use_as_background FROM ir_attachment WHERE id = ANY (%s)', (ids,))
            for id, use_as_background in cr.fetchall():
                if use_as_background:
                    ids.remove(id)
            if not ids:
                return
        return super(IRAttachmentBackground, self).check(mode, values=values)
