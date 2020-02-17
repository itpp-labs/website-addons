# Copyright 2016 Ilyas <https://github.com/ilyasProgrammer>
# Copyright 2016 Ildar Nasyrov <https://www.it-projects.info/team/iledarn>
# Copyright 2016 Dinar Gabbasov <https://www.it-projects.info/team/GabbasovDinar>
# Copyright 2016-2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2017 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    buy_way = fields.Char()
    payment_method_information = fields.Char(
        compute="_compute_payment_method_information"
    )
    delivery_method_information = fields.Char(
        compute="_compute_delivery_method_information"
    )
    payment_acquirer_id = fields.Many2one(
        "payment.acquirer",
        string="Payment Acquirer",
        compute="_compute_payment_acquirer_id",
    )

    def _compute_payment_method_information(self):
        self.payment_method_information = False
        if str(self.buy_way) == "nobill_ship":
            self.payment_method_information = _("Pay on delivery")
        elif str(self.buy_way) == "nobill_noship":
            self.payment_method_information = _("Pay at store")

    def _compute_delivery_method_information(self):
        self.delivery_method_information = False
        if str(self.buy_way) == "bill_noship" or str(self.buy_way) == "nobill_noship":
            self.delivery_method_information = _("Pickup at store")

    def _compute_payment_acquirer_id(self):
        self.payment_acquirer_id = self.get_portal_last_transaction().acquirer_id

    def get_shipping_billing(self):
        if not self.buy_way:
            return {
                "ship_enabled": "1",
                "bill_enabled": "1",
            }
        return {
            "ship_enabled": "noship" not in self.buy_way and "1" or "0",
            "bill_enabled": "nobill" not in self.buy_way and "1" or "0",
        }

    def remove_is_delivery(self):
        for line in self.order_line:
            if hasattr(line, "is_delivery") and line.is_delivery:
                line.unlink()

    def recalc_has_delivery(self):
        if hasattr(self, "_compute_has_delivery"):
            if self.buy_way and "noship" in self.buy_way:
                self.has_delivery = False
            else:
                self._compute_has_delivery()


class WebsiteConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    nobill_noship = fields.Boolean("Pickup and pay at store")
    bill_noship = fields.Boolean("Pickup at store but pay now")
    bill_ship = fields.Boolean("Pay now and get delivery")
    nobill_ship = fields.Boolean("Pay on delivery")
    bill_ship_option = fields.Selection(
        [
            ("nobill_noship", "Pickup and pay at store"),
            ("bill_noship", "Pickup at store but pay now"),
            ("bill_ship", "Pay now and get delivery"),
            ("nobill_ship", "Pay on delivery"),
        ],
        string="Selected by default",
        default="nobill_noship",
    )

    @api.model
    def get_values(self):
        res = super(WebsiteConfigSettings, self).get_values()
        config_parameters = self.env["ir.config_parameter"].sudo()
        res.update(
            nobill_noship=config_parameters.get_param(
                "website_sale_checkout_store.nobill_noship", default=False
            ),
            bill_noship=config_parameters.get_param(
                "website_sale_checkout_store.bill_noship", default=False
            ),
            bill_ship=config_parameters.get_param(
                "website_sale_checkout_store.bill_ship", default=False
            ),
            nobill_ship=config_parameters.get_param(
                "website_sale_checkout_store.nobill_ship", default=False
            ),
            bill_ship_option=config_parameters.get_param(
                "website_sale_checkout_store.bill_ship_option", default="nobill_noship"
            ),
        )
        return res

    def set_values(self):
        super(WebsiteConfigSettings, self).set_values()
        config_parameters = self.env["ir.config_parameter"].sudo()
        for record in self:
            config_parameters.set_param(
                "website_sale_checkout_store.nobill_noship", record.nobill_noship or ""
            )
            config_parameters.set_param(
                "website_sale_checkout_store.bill_noship", record.bill_noship or ""
            )
            config_parameters.set_param(
                "website_sale_checkout_store.bill_ship", record.bill_ship or ""
            )
            config_parameters.set_param(
                "website_sale_checkout_store.nobill_ship", record.nobill_ship or ""
            )
            config_parameters.set_param(
                "website_sale_checkout_store.bill_ship_option",
                record.bill_ship_option or "",
            )
