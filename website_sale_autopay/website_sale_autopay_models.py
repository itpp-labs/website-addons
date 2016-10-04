# -*- coding: utf-8 -*-
from openerp import fields, api
from openerp import models
import re


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    journal_id = fields.Many2one('account.journal', 'Payment method', help='This journal is used to auto pay invoice when online payment is received')

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            return {'domain': {'journal_id': [('company_id', '=', self.company_id.id)]}}


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def action_button_confirm(self, cr, uid, ids, context=None):
        super(SaleOrder, self).action_button_confirm(cr, uid, ids, context=context)
        r = self.browse(cr, uid, ids[0], context=context)
        if r.payment_tx_id and r.payment_tx_id.state == 'done' and r.payment_acquirer_id:
            r._autopay()

    def _autopay(self, cr, uid, ids, context=None):
            # Keep old indent to don't touch git history
            r = self.browse(cr, uid, ids[0], context=context)

            sale_order_company = r.company_id
            user_company = self.pool['res.users'].browse(cr, uid, uid, context=context).company_id
            self.pool['res.users'].write(cr, uid, uid, {'company_id': sale_order_company.id})

            journal_id = r.payment_acquirer_id.journal_id.id or self.pool['account.invoice'].default_get(cr, uid, ['journal_id'], context=context)['journal_id']

            # [create invoice]
            res = self.pool['sale.order'].manual_invoice(cr, uid, [r.id], context)
            invoice_id = res['res_id']

            # [validate]
            self.pool['account.invoice'].signal_workflow(cr, uid, [invoice_id], 'invoice_open')

            # [register payment]
            res = self.pool['account.invoice'].invoice_pay_customer(cr, uid, [invoice_id], context=context)
            voucher_context = res['context']

            update = {}
            for dkey in voucher_context:
                if not dkey.startswith('default_'):
                    continue
                key = re.sub(r'^default_', '', dkey)
                if voucher_context.get(key):
                    continue
                update[key] = voucher_context[dkey]
            voucher_context.update(update)

            field_list = ["comment", "line_cr_ids", "is_multi_currency", "paid_amount_in_company_currency", "line_dr_ids", "journal_id", "currency_id", "narration", "partner_id", "payment_rate_currency_id", "reference", "writeoff_acc_id", "state", "pre_line", "type", "payment_option", "account_id", "company_id", "period_id", "date", "payment_rate", "name", "writeoff_amount", "analytic_id", "amount"]
            voucher_values = self.pool['account.voucher'].default_get(cr, uid, field_list, context=voucher_context)

            res = self.pool['account.voucher'].onchange_journal(
                # in case we want to register the payment directly from an invoice, it's confusing to allow to switch the journal
                # without seeing that the amount is expressed in the journal currency, and not in the invoice currency. So to avoid
                # this common mistake, we simply reset the amount to 0 if the currency is not the invoice currency.
                cr, uid, False,

                journal_id,
                [],  # line_ids
                False,  # tax_id
                voucher_values.get('partner_id'),
                voucher_values.get('date'),
                voucher_values.get('amount'),
                voucher_values.get('type'),
                voucher_values.get('company_id'),

                context=voucher_context)
            voucher_values.update(res['value'])
            voucher_values.update({'journal_id': journal_id})

            for key in ['line_dr_ids', 'line_cr_ids']:
                array = []
                for obj in voucher_values[key]:
                    array.append([0, False, obj])
                voucher_values[key] = array
            voucher_id = self.pool['account.voucher'].create(cr, uid, voucher_values, context=voucher_context)

            # [pay]
            self.pool['account.voucher'].button_proforma_voucher(cr, uid, [voucher_id], context=voucher_context)

            # return user company to its original value
            self.pool['res.users'].write(cr, uid, uid, {'company_id': user_company.id})
