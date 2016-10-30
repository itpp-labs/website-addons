# -*- coding: utf-8 -*-

from odoo.http import request
import openerp.addons.website_sale.controllers.main as main


class WebsiteSaleBirthdate(main.WebsiteSale):

    def checkout_values(self, data=None):

        values = super(WebsiteSaleBirthdate, self).checkout_values(data)

        current_user = request.env.user

        # if user is activated
        if current_user.active:
            partner_birthdate = current_user.partner_id.birthdate

            if partner_birthdate:
                values['checkout']['birthdate'] = partner_birthdate

        return values

    def checkout_parse(self, address_type, data, remove_prefix=False):

        val = super(WebsiteSaleBirthdate, self).checkout_parse(address_type, data, remove_prefix)

        if address_type == 'billing':
            val['birthdate'] = data['birthdate']

        return val

    def checkout_form_validate(self, data):

        error = super(WebsiteSaleBirthdate, self).checkout_form_validate(data)

        if not data.get('birthdate'):
            error['birthdate'] = 'missing'

        return error
