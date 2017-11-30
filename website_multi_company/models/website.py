# -*- coding: utf-8 -*-
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"

    def multi_theme_reload(self):
        self.env['res.config.settings'].multi_theme_reload()
