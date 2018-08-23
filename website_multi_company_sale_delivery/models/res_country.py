# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCountry(models.Model):
    _inherit = 'res.country'

    def get_website_sale_countries(self, mode='billing'):
        res = super(ResCountry, self).get_website_sale_countries(mode=mode)
        if mode == 'shipping':
            countries = self.env['res.country']
            public_user = self.env.ref('base.public_user')
            delivery_carriers = self.env['delivery.carrier'].sudo(public_user).search([('website_published', '=', True)])
            for carrier in delivery_carriers:
                if not carrier.country_ids and not carrier.state_ids:
                    countries = res
                    break
                countries |= carrier.country_ids

            res = res & countries
        return res

    def get_website_sale_states(self, mode='billing'):
        res = super(ResCountry, self).get_website_sale_states(mode=mode)

        states = self.env['res.country.state']
        if mode == 'shipping':
            dom = ['|', ('country_ids', 'in', self.id), ('country_ids', '=', False), ('website_published', '=', True)]
            public_user = self.env.ref('base.public_user')
            delivery_carriers = self.env['delivery.carrier'].sudo(public_user).search(dom)

            for carrier in delivery_carriers:
                if not carrier.country_ids and not carrier.state_ids:
                    states = res
                    break
                states |= carrier.state_ids
            if not states:
                states = states.search([('country_id', '=', self.id)])
            res = res & states
        return res
