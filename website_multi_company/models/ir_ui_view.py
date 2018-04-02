# -*- coding: utf-8 -*-
# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

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
            raise AccessError(_('You are trying to edit the %r website but can only edit the %r websites. Please contact your system administrator') % (self.website_id.name, self.env.user.editor_website_ids.mapped('name')))
