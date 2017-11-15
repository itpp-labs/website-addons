# -*- coding: utf-8 -*-
from odoo import api, fields, models


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
                    partner_by_email = self.env['res.partner'].search([('email', '=ilike', vals.get('email'))], limit=1)
                    if partner_by_email:
                        vals['partner_id'] = partner_by_email.id
                    else:
                        # If email differs from current user
                        # and partner doesn't exist
                        # THEN
                        # delete it to force event_partner module to create new partner for this attendee
                        del vals['partner_id']
                        update_partner = False

        res = super(EventRegistration, self).create(vals)

        if res.partner_id:
            if update_partner:
                res.partner_id.write(
                    self._prepare_partner(vals)
                )
            # be sure, that name and phone in registration are ones from Contact and not from Agent
            res.name = res.partner_id.name
            res.phone = res.partner_id.phone

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
