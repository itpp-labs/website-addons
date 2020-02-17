# Copyright 2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

import logging
import re

from odoo import _, api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
# from https://stackoverflow.com/a/26987741/222675
DOMAIN_REGEXP = r"^(((?!-))(xn--|_{1,1})?[a-z0-9-]{0,61}[a-z0-9]{1,1}\.)*(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$"


class Website(models.Model):
    _inherit = "website"

    @api.multi
    def multi_theme_reload(self):
        self.ensure_one()

        # convert_assets and copy views for current website
        self._multi_theme_activate()

    @api.multi
    def multi_theme_reload_list(self):
        # only reloads list
        self.env["website.theme"].search([])._convert_assets()

    @api.multi
    def _multi_theme_activate(self):
        if not self.env.context.get("skip_converting_assets"):
            # reload dependencies before activating
            self.mapped("multi_theme_id").upstream_dependencies()._convert_assets()
        return super(Website, self)._multi_theme_activate()

    @api.constrains("domain")
    def _check_domain(self):
        if self.domain and not re.match(DOMAIN_REGEXP, self.domain):
            if "/" in self.domain:
                msg = _("Don't use slash symbol for domain")
            else:
                msg = _("Not a valid domain")

            raise ValidationError(msg)
