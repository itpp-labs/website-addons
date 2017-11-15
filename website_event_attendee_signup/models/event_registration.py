# -*- coding: utf-8 -*-
from odoo import api, fields, models, exceptions, _


class EventRegistration(models.Model):
    _inherit = "event.registration"

    agent_id = fields.Many2one(
        'res.partner', string='Agent',
        states={'done': [('readonly', True)]},
        help="A person who purchased the registration",
    )

    @api.model
    def create(self, vals):
        event = self.env['event.event'].browse(vals['event_id'])

        partner = vals.get('partner_id')
        update_partner = True
        if partner:
            vals['agent_id'] = partner

            if event.create_partner:
                partner = self.env['res.partner'].browse(partner)
                if vals.get('email') != partner.email:
                    # delete it to force event_partner module to create new partner for this attendee
                    del vals['partner_id']
                    update_partner = False

        res = super(EventRegistration, self).create(vals)

        if res.partner_id and update_partner:
            res.partner_id.write(
                self._prepare_partner(vals)
            )

        if res.event_id.attendee_signup and res.partner_id:
            login = res.partner_id.email
            user = self.env['res.users']\
                       .search([('login', '=ilike', login)])
            if not user:
                user = self.env['res.users']\
                           ._signup_create_user({
                               'login': login,
                               'partner_id': res.partner_id.id,
                           })
                user.partner_id.signup_prepare()

        return res
