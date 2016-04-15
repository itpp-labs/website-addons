# -*- coding: utf-8 -*-

import openerp
from openerp.addons.payment.models.payment_acquirer import ValidationError
from openerp.addons.payment.tests.common import PaymentAcquirerCommon
from openerp.tools import mute_logger
from openerp.tests import common

@openerp.tests.common.at_install(True)
@openerp.tests.common.post_install(True)
class AuthorizeForm(PaymentAcquirerCommon):

    @mute_logger('openerp.addons.payment_authorize.models.authorize', 'ValidationError')
    def test_10_go(self):
        cr, uid, context = self.env.cr, self.env.uid, {}
        # authorize only support USD in test environment
        self.currency_usd = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)[0]
        # get the authorize account
        model, self.authorize_id = self.env['ir.model.data'].get_object_reference('payment_authorize', 'payment_acquirer_authorize')
        # Usefull models
        self.ir_model_data = self.registry('ir.model.data')
        self.sale_order_line = self.registry('sale.order.line')
        self.sale_order = self.registry('sale.order')
        self.product = self.registry('product.product')

        # product that has a phantom bom
        self.product_bom_id = \
        self.ir_model_data.get_object_reference(cr, uid, 'product', 'product_product_3')[1]
        # partner agrolait
        self.partner_id = self.ir_model_data.get_object_reference(cr, uid, 'base', 'res_partner_1')[1]

        # be sure not to do stupid thing
        authorize = self.env['payment.acquirer'].browse(self.authorize_id)
        self.assertEqual(authorize.environment, 'test', 'test without test environment')

        # typical data posted by authorize after client has successfully paid
        authorize_post_data = {
            'return_url': u'/shop/payment/validate',
            'x_MD5_Hash': u'7934485E1C105940BE854208D10FAB4F',
            'x_account_number': u'XXXX0027',
            'x_address': u'Huge Street 2/543',
            'x_amount': u'450.00',
            'x_auth_code': u'E4W7IU',
            'x_avs_code': u'Y',
            'x_card_type': u'Visa',
            'x_cavv_response': u'2',
            'x_city': u'Sun City',
            'x_company': u'',
            'x_country': u'Belgium',
            'x_cust_id': u'',
            'x_cvv2_resp_code': u'',
            'x_description': u'',
            'x_duty': u'0.00',
            'x_email': u'norbert.buyer@exampl',
            'x_fax': u'',
            'x_first_name': u'Norbert',
            'x_freight': u'0.00',
            'x_invoice_num': u'SO004',
            'x_last_name': u'Buyer',
            'x_method': u'CC',
            'x_phone': u'0032 12 34 56 78',
            'x_po_num': u'',
            'x_response_code': u'1',
            'x_response_reason_code': u'1',
            'x_response_reason_text': u'This transaction has been approved.',
            'x_ship_to_address': u'Huge Street 2/543',
            'x_ship_to_city': u'Sun City',
            'x_ship_to_company': u'',
            'x_ship_to_country': u'Belgium',
            'x_ship_to_first_name': u'Norbert',
            'x_ship_to_last_name': u'Buyer',
            'x_ship_to_state': u'',
            'x_ship_to_zip': u'1000',
            'x_state': u'',
            'x_tax': u'0.00',
            'x_tax_exempt': u'FALSE',
            'x_test_request': u'false',
            'x_trans_id': u'2217460311',
            'x_type': u'auth_capture',
            'x_zip': u'1000'
        }

        # should raise error about unknown tx
        with self.assertRaises(ValidationError):
            self.payment_transaction.form_feedback(cr, uid, authorize_post_data, 'authorize', context=context)

        #create sale order with one sale order line containing product with a phantom bom
        so_id = self.sale_order.create(cr, uid, vals={'partner_id': self.partner_id}, context=context)
        self.sale_order_line.create(cr, uid, values={'order_id': so_id, 'product_id': self.product_bom_id, 'product_uom_qty': 1}, context=context)
        tx = self.env['payment.transaction'].create({
            'amount': 450.0,
            'acquirer_id': self.authorize_id,
            'currency_id': self.currency_usd.id,
            'reference': 'SO004',
            'partner_name': 'Norbert Buyer',
            'sale_order_id': so_id,
            'state': 'done',
            'partner_country_id': self.country_france_id})
        self.sale_order.write(
            cr, uid, [so_id], {
                'payment_acquirer_id': self.authorize_id,
                'payment_tx_id': tx.id
            }, context=context)

        # validate it
        self.payment_transaction.form_feedback(cr, uid, authorize_post_data, 'authorize', context=context)
        created_invoice_id = self.env['sale.order'].browse(so_id).invoice_ids[0].id
        created_ivoice = self.env['account.invoice'].browse(created_invoice_id)
        self.assertEqual(created_ivoice.state, 'paid', 'Invoice state wrong')

