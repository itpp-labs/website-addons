from odoo import api, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model
    def create(self, vals):
        res = super(EventRegistration, self).create(vals)

        if res.event_id.attendee_signup and res.attendee_partner_id:
            login = res.attendee_partner_id.email
            user = self.env["res.users"].search([("login", "=ilike", login)])
            if not user:
                user = (
                    self.env["res.users"]
                    .sudo()
                    ._signup_create_user(
                        {"login": login, "partner_id": res.attendee_partner_id.id}
                    )
                )
                user.partner_id.signup_prepare()

        return res
