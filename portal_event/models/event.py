# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.http import request


class Event(models.Model):
    _inherit = 'event.event'

    @api.multi
    def check_partner_for_new_ticket(self, partner_id):
        registration = self.partner_is_participating(partner_id)
        if registration:
            ticket_order_lines = registration.mapped('sale_order_line_id')

            cart_refund_lines = request.website.sale_get_order().order_line.mapped(lambda r: r.refund_source_line_id)
            # all refund lines must be in ticket_order_lines
            if all([line in cart_refund_lines for line in ticket_order_lines]):
                # False means no errors
                return False

        return super(Event, self).check_partner_for_new_ticket(partner_id)
