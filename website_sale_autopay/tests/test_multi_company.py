# -*- coding: utf-8 -*-
import logging
from openerp.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestMultiCompany(TransactionCase):
    at_install = False
    post_install = True

    def _test_order(self, order):
        order.action_confirm()
        order._autopay()
        self.assertTrue(order.invoice_status == 'invoiced', 'Order state is not paid after _autopay. State=%s' % order.state)

    def test_10_default_company(self):
        """Check simplest case without switching company"""
        order = self.env.ref('website_sale_autopay.sale_order_1')
        self._test_order(order)

    def test_20_another_company(self):
        # Odoo Us company should be in list of Allowed Companies for Administrator user
        # It also requires generated accounts for the multi_company.res_company_oirp_us company
        # * From ``Settings / Configuration / Invoicing`` menu ``Select Company`` field choose ``Odoo US`` company
        # * Select any chart of account template on ``Template`` field
        # * On ``Default company currency`` select currency such as all your companies have the same currency
        # * Push ``Apply`` button.
        # Now that you have accounts for ``Odoo BE`` company with proper currency, you can start testing
        order = self.env.ref('website_sale_autopay.sale_order_1')
        company = self.env.ref('website_sale_autopay.res_company_oerp_us', raise_if_not_found=False)
        prop = self.env['ir.property']
        rec_dom = [('name', '=', 'property_account_receivable_id'), ('company_id', '=', company.id)]
        pay_dom = [('name', '=', 'property_account_payable_id'), ('company_id', '=', company.id)]
        res_dom = [('res_id', '=', 'res.partner,%s' % self.env.user.partner_id)]
        rec_prop = prop.search(rec_dom + res_dom) or prop.search(rec_dom)
        pay_prop = prop.search(pay_dom + res_dom) or prop.search(pay_dom)
        rec_account = rec_prop.get_by_record(rec_prop)
        pay_account = pay_prop.get_by_record(pay_prop)
        if not rec_account and not pay_account:
            _logger.info('Cannot find a chart of accounts for test company, You should configure it. \nPlease go to Account Configuration.')
            return
        for line in order.order_line:
            line.product_id.company_id = company.id
        order.company_id = company.id
        self.assertEqual(order.company_id.id, company.id, 'Demo data are wrong')
        self._test_order(order)
