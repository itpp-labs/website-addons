from odoo import models


class Website(models.Model):

    _inherit = "website"

    def init(self):
        # We cannot do it via xml due to noupdate="1", so do it here
        #
        # <record id="website.homepage_page" model="website.page">
        # <field name="website_ids" eval="[(6, 0, [ref('website.default_website')])]"/>
        # </record>
        self.env.ref("website.homepage_page").write(
            {"website_ids": [(6, 0, [self.env.ref("website.default_website").id])]}
        )
