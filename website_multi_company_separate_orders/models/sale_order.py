# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_parent_id = fields.Many2one('sale.order', 'Parent Order', readonly=True)
    order_child_ids = fields.One2many('sale.order', 'order_parent_id', 'Child Orders', readonly=True)

    @api.multi
    def action_done(self):
        result = super(SaleOrder, self).action_done()
        children = self.mapped('order_child_ids')
        if children:
            children.action_done()
        return result

    @api.multi
    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        children = self.mapped('order_child_ids')
        if children:
            children.action_confirm()
        return result

    @api.multi
    def action_cancel(self):
        result = super(SaleOrder, self).action_cancel()
        children = self.mapped('order_child_ids')
        if children:
            children.action_cancel()
        return result

    @api.multi
    def write(self, values):
        result = super(SaleOrder, self).write(values)
        if 'partner_id' in values:
            for record in self:
                if record.order_child_ids:
                    record.order_child_ids.write({
                        'partner_id': values['partner_id'],
                        'partner_invoice_id': values['partner_id'],
                        'partner_shipping_id': values['partner_id'],
                    })
        return result


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def register_payment(self, payment_line, writeoff_acc_id=False, writeoff_journal_id=False):
        result = super(AccountInvoice, self).register_payment(payment_line, writeoff_acc_id, writeoff_journal_id)
        for record in self:
            if record.state != 'paid':
                return result
            sale_line_ids = record.invoice_line_ids[0].sale_line_ids
            if sale_line_ids:
                order = sale_line_ids[0].order_id.sudo()
                children = order.order_child_ids.filtered(lambda o: o.invoice_status not in ['cancel', 'invoiced'])
                if children:
                    children.action_cancel()
                parent = order.order_parent_id
                if parent:
                    product_ids = order.order_line.mapped(lambda ol: ol.product_id.id)
                    order_line_ids = parent.order_line.filtered(lambda ol: ol.product_id.id in product_ids)
                    order_line_ids.write({
                        'product_uom_qty': 0,
                    })
        return result
