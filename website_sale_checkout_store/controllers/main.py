# Copyright 2016 Ilyas <https://github.com/ilyasProgrammer>
# Copyright 2016-2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2017 Dmytro Katyukha <https://github.com/katyukha>
# Copyright 2017-2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleExtended(WebsiteSale):
    @http.route()
    def address(self, **post):
        # checks for module website_sale_delivery and turn off delivery for the order in both noship options
        address_super = super(WebsiteSaleExtended, self).address(**post)
        address_super.qcontext.update(
            request.website.sale_get_order().get_shipping_billing()
        )
        return address_super

    @http.route()
    def checkout(self, **post):
        order = request.website.sale_get_order()
        checkout_super = super(WebsiteSaleExtended, self).checkout(**post)
        try:
            order.buy_way = post["buyMethod"]
        except Exception:
            pass
        if not checkout_super.location:
            # no need to update variables if super does a redirection
            order.recalc_has_delivery()
            if str(order.buy_way) == "nobill_noship":
                # in nobill_noship case omits checkout page step and redirects to shop/payment
                # which in nobill case resets website order data and redirects to confirmation
                return request.redirect("/shop/payment")
            checkout_super.qcontext.update(order.get_shipping_billing())
        return checkout_super

    @http.route()
    def payment(self, **post):
        order = request.website.sale_get_order()
        order.recalc_has_delivery()
        if order.buy_way:
            data = order.get_shipping_billing()
            if "noship" in order.buy_way:
                order.remove_is_delivery()
                data["deliveries"] = False
            if "nobill" in order.buy_way:
                request.session["sale_last_order_id"] = order.id

            payment_super = super(WebsiteSaleExtended, self).payment(**post)
            payment_super.qcontext.update(data)
        return payment_super

    @http.route()
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        order = request.website.sale_get_order()
        if order.buy_way and "nobill" in order.buy_way:
            self.reset_order()
            return request.redirect("/shop/confirmation")
        return super(WebsiteSaleExtended, self).payment_validate(
            transaction_id, sale_order_id, **post
        )

    @http.route()
    def payment_get_status(self, sale_order_id, **post):
        order = request.env["sale.order"].sudo().browse(sale_order_id)
        if order.buy_way and "nobill" in order.buy_way:
            return {"recall": False, "message": ""}
        else:
            return super(WebsiteSaleExtended, self).payment_get_status(
                sale_order_id, **post
            )

    def reset_order(self):
        order = request.website.sale_get_order()
        order.force_quotation_send()
        request.website.sale_reset()

    def _get_mandatory_fields(self):
        order = request.website.sale_get_order()
        if not order.buy_way or "noship" not in order.buy_way:
            return ["name", "phone", "email", "street", "city", "country_id"]
        else:
            if "nobill" in order.buy_way:
                return ["name", "phone", "email"]
            else:
                return ["name", "phone", "email", "country_id"]

    def _get_mandatory_billing_fields(self):
        return self._get_mandatory_fields()

    def _get_mandatory_shipping_fields(self):
        return self._get_mandatory_fields(shipping=True)
