# -*- coding: utf-8 -*-
from openerp import fields
from openerp import models
import logging
import re

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    payment_acquirer_id = fields.Many2one('payment.acquirer', 'Payment acquirer')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_button_confirm(self, cr, uid, ids, context=None):
        super(SaleOrder, self).action_button_confirm(cr, uid, ids, context=context)
        r = self.browse(cr, uid, ids[0], context=context)
        if r.payment_tx_id and r.payment_tx_id.state == 'done' and r.payment_acquirer_id:
            journal_ids = self.pool['account.journal'].search(cr, uid,
                                                              [('company_id', '=', r.company_id.id),
                                                               ('payment_acquirer_id', '=',
                                                                r.payment_acquirer_id.id)])
            if not journal_ids:
                _logger.warning("No journal for company_id %s and payment_acquirer_id %s.", r.company_id.id, r.payment_acquirer_id.id)
                return
            else:
                journal_id = journal_ids[0]

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
            print 'voucher_id', voucher_id

            # [pay]
            self.pool['account.voucher'].button_proforma_voucher(cr, uid, [voucher_id], context=voucher_context)
