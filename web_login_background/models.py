# -*- coding: utf-8 -*-
from random import choice
import hashlib

from odoo import fields, api
from odoo import models


def _attachment2url(att):
    sha = hashlib.sha1(getattr(att, '__last_update')).hexdigest()[0:7]
    return '/web/image/%s-%s' % (att.id, sha)


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

    @api.model
    def get_background_pic(self):
        pictures = self.search([('use_as_background', '=', True)])
        if pictures:
            p = choice(pictures)
            picture_url = p.url or _attachment2url(p)
            return picture_url
        else:
            return False
