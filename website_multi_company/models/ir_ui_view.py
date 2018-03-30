# -*- coding: utf-8 -*-

import logging

from odoo import api, models, _
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


class View(models.Model):
    _inherit = 'ir.ui.view'

    @api.multi
    def check_access_rule(self, operation):
        super(View, self).check_access_rule(operation)
        if operation == 'write' and self.env.user.editor_website_ids and self.mapped('website_id') - self.env.user.editor_website_ids:
            _logger.info('Current user, uid: %s cannot write to the websites: %r', self._uid, self.mapped('website_id') - self.env.user.editor_website_ids)
            raise AccessError(_('The requested operation cannot be completed due to security restrictions. Please contact your system administrator.\n\n(Document type: %s, Operation: %s)') % (self._description, 'write'))
