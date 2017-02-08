# -*- coding: utf-8 -*-
from odoo import fields, api
from odoo import models


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    journal_id = fields.Many2one('account.journal', 'Payment method', help='This journal is used to auto pay invoice when online payment is received')

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            return {'domain': {'journal_id': [('company_id', '=', self.company_id.id)]}}


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        [r._autopay()
         for r in self
         if r.payment_tx_id and
         r.payment_tx_id.state == 'done' and
         r.payment_acquirer_id]

        return res

    @api.multi
    def _autopay(self):
            # Keep old indent to don't touch git history
            self.ensure_one()
            r = self

            sale_order_company = r.company_id
            user_company = self.env.user.company_id
            self.env.user.write({'company_id': sale_order_company.id})

            journal_id = r.payment_acquirer_id.journal_id.id or self.env['account.invoice'].default_get(['journal_id'])['journal_id']

            for m in r.order_line:
                m.qty_to_invoice = m.product_uom_qty

            res = r.action_invoice_create()
            invoice_id = res[0]

            # [validate]
            invoice_obj = r.env['account.invoice'].browse(invoice_id)
            journal_obj = r.env['account.journal'].browse(journal_id)
            invoice_obj.action_invoice_open()

            # [register payment]
            invoice_obj.pay_and_reconcile(journal_obj, invoice_obj.amount_total)
            invoice_obj.action_move_create()
            invoice_obj.action_invoice_paid()

            # return user company to its original value
            self.env.user.write({'company_id': user_company.id})
