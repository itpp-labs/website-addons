# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID
from odoo import models


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def form_feedback(self, data, acquirer_name):
        super(PaymentTransaction, self).form_feedback(data, acquirer_name)

        tx = None
        # fetch the tx, check its state, confirm the potential SO
        tx_find_method_name = '_%s_form_get_tx_from_data' % acquirer_name
        if hasattr(self, tx_find_method_name):
            tx = getattr(self, tx_find_method_name)(data)
        if tx:
            self.env['sale.order'].action_button_confirm([tx.sale_order_id.id])

        return True
