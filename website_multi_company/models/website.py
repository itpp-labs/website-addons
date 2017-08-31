# -*- coding: utf-8 -*-
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"

    def multi_theme_reload(self):
        """Update multiwebsite themes when loading a new wizard."""
        _logger.info("Reloading available multi-website themes")
        # Reload available single-website converted themes
        self.env["website.theme"].search([])._convert_assets()
        # Reload custom views for themes activated in any website
        self.env["website"].search([])._multi_theme_activate()
