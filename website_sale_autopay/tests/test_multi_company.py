# -*- coding: utf-8 -*-
import logging
from openerp.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestMultiCompany(TransactionCase):
    at_install = False
    post_install = True

    def _test_order(self, order):
        order.action_button_confirm()
        order._autopay()
        self.assertTrue(order.invoiced, 'Order state is not paid after _autopay. State=%s' % order.state)

    def test_10_default_company(self):
        """Check simplest case without switching company"""
        order = self.env.ref('website_sale_autopay.sale_order_1')
        self._test_order(order)

    def test_20_another_company(self):
        # This test requires the multi_company module
        # It also requires generated accounts for the multi_company.res_company_oirp_be company
        # * Install multi_company
        # * From ``Settings / Configuration / Invoicing`` menu ``Select Company`` field choose ``Odoo BE`` company
        # * Select any chart of account template on ``Template`` field
        # * On ``Default company currency`` select currency such as all your companies have the same currency
        # * Push ``Apply`` button.
        # Now that you have accounts for ``Odoo BE`` company with proper currency, you can start testing
        order = self.env.ref('website_sale_autopay.sale_order_1')
        company = self.env.ref('multi_company.res_company_oerp_be', raise_if_not_found=False)
        if not company:
            _logger.info("Install multi_company module to run this test")
            return
        for line in order.order_line:
            line.product_id.company_id = company.id
        order.company_id = company.id
        self.assertEqual(order.company_id.id, company.id, 'Demo data are wrong')
        self._test_order(order)
