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
        print 'SIGNUP: create: partner=%s' % partner
        if partner:
            vals['agent_id'] = partner

            if event.create_partner:
                partner = self.env['res.partner'].browse(partner)
                if vals.get('email') != partner.email:
                    # delete it to force event_partner module to create new partner for this attendee
                    del vals['partner_id']

        res = super(EventRegistration, self).create(vals)

        if res.event_id.attendee_signup and res.partner_id:
            # no_reset_password means don't send invitation email with standart template
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
            template = self.env.ref('website_event_attendee_signup.email_template_signup')
            res.message_post_with_template(template.id, composition_mode='comment')

        return res
