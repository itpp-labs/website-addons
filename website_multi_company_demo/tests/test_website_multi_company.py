# -*- coding: utf-8 -*-
from odoo.tests.common import SingleTransactionCase, get_db_name, at_install, post_install
from ..models.res_users import WEBSITE_REFS
from odoo.api import Environment

db_name = get_db_name()


@at_install(False)
@post_install(True)
class TestWebsiteMultiCompany(SingleTransactionCase):

    def _test_website_price_difference_is_accessible(self, env):
        website = env.ref(WEBSITE_REFS[0])
        products = env['product.template'].search(
            [('company_id', '=', website.company_id.id)] +
            website.sale_product_domain()
        )
        product = products[0]
        product.website_price_difference  # make sure, it does not throw exception

    def test_website_price_difference_is_accessible_for_demo_user(self):
        uid = self.registry['res.users'].authenticate(db_name, 'demo', 'demo', {})
        with self.cursor() as cr:
            env = Environment(cr, uid, {})
            self._test_website_price_difference_is_accessible(env)

    def test_website_price_difference_is_accessible_for_public_user(self, env=None):
        self._test_website_price_difference_is_accessible(self.env(user=self.browse_ref('base.public_user')))
