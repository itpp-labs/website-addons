import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class WebsiteTheme(models.Model):
    _inherit = 'website.theme'

    name = fields.Char(string="Theme")
    converted_theme_addon = fields.Char(
        string="Theme's technical name",
        help="")

    dependency_ids = fields.Many2many(
        'ir.module.module',
        string="Dependencies",
        help='Theme-like dependencies. Add modules here if you got error "The style compilation failed".')

    def _convert_assets(self):
        """Generate assets for converted themes"""
        Asset = self.env["website.theme.asset"]
        for one in self.filtered("converted_theme_addon"):
            # Get all views owned by the converted theme addon
            refs = self.env["ir.model.data"].search([
                ("module", "in", [one.converted_theme_addon] + one.dependency_ids.mapped('name')),
                ("model", "=", "ir.ui.view"),
            ])
            existing = frozenset(one.mapped("asset_ids.name"))
            expected = frozenset(refs.mapped("complete_name"))
            dangling = tuple(existing - expected)
            # Create a new asset for each theme view
            for ref in expected - existing:
                _logger.debug("Creating asset %s for theme %s", ref, one.name)

                view = self.env.ref(ref, raise_if_not_found=False)
                if view and view.type != 'qweb':
                    # skip backend views
                    continue

                one.asset_ids |= Asset.new({
                    "name": ref,
                })
            # Delete all dangling assets
            if dangling:
                _logger.debug(
                    "Removing dangling assets for theme %s: %s",
                    one.name, dangling)
                Asset.search([("name", "in", dangling)]).unlink()
        # Turn all assets multiwebsite-only
        Asset._find_and_deactivate_views()
