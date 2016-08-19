# -*- coding: utf-8 -*-
from openerp import fields
from openerp import models
import re


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    journal_id = fields.Many2one('account.journal', 'Payment method', help='This journal is used to auto pay invoice when online payment is received')


class sale_order(models.Model):

    _inherit = 'sale.order'

    def action_confirm(self, cr, uid, ids, context=None):
        super(sale_order, self).action_confirm(cr, uid, ids, context=context)
        r = self.browse(cr, uid, ids[0], context=context)
        if r.payment_tx_id and r.payment_tx_id.state == 'done' and r.payment_acquirer_id:
            journal_id = r.payment_acquirer_id.journal_id.id or self.pool['account.invoice'].default_get(cr, uid, ['journal_id'], context=context)['journal_id']

            for m in r.order_line:
                m.qty_to_invoice = m.product_uom_qty

            res = r.pool['sale.order'].action_invoice_create(cr, uid, [r.id], context)
            invoice_id = res[0]

            # [validate]
            invoice_obj = r.env['account.invoice'].browse(invoice_id)
            journal_obj = r.env['account.journal'].browse(journal_id)
            invoice_obj.signal_workflow('invoice_open')

            # [register payment]
            invoice_obj.pay_and_reconcile(journal_obj, invoice_obj.amount_total)
            invoice_obj.action_move_create()
            invoice_obj.confirm_paid()
