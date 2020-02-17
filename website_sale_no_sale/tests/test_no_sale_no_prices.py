# Copyright 2018 Denis Mudarisov <https://it-projects.info/team/trojikman>
# License MIT (https://opensource.org/licenses/MIT).

import odoo.tests
from odoo import api


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):
    def enable_environment(self, template_id):
        self.phantom_env = api.Environment(self.registry.test_cr, self.uid, {})
        settings = self.phantom_env["res.config.settings"]
        # a reload is needed for the module to work correctly with multi themes
        if hasattr(settings, "multi_theme_reload"):
            settings.multi_theme_reload()
        self.phantom_env["ir.ui.view"].search(
            [("active", "=", False), ("website_id", "=", 1), ("key", "=", template_id)]
        ).write({"active": True})

    def disable_conflict_module(self, template_id):
        custom_website_view = self.phantom_env["ir.ui.view"].search(
            [("active", "=", True), ("key", "=", template_id)]
        )
        if custom_website_view:
            custom_website_view.write({"active": False})

    def test_01_remove_products_prices(self):
        self.enable_environment("website_sale_no_sale.hide_products_prices")
        url = "/shop"
        code = """
                    if ($('[data-oe-expression="product.website_price"]').length > 0) {

                        console.log('error', 'Prices is not removed');
                    } else {
                        console.log('ok');
                    }
        """
        self.phantom_js(url, code, login="demo", ready="$('.product_price')")

    def test_02_remove_add_to_cart(self):
        self.enable_environment("website_sale_no_sale.hide_add_to_cart")
        self.disable_conflict_module("website_sale_add_to_cart.product")
        url = "/shop/product/ipod-20"
        code = """
                    if ($('#add_to_cart').hasClass('o_hidden')) {
                        console.log('ok');
                    } else {
                        console.log('error', 'Add to cart button is not removed');
                    }
        """
        self.phantom_js(url, code, login="demo", ready="$('#product_details')")

    def test_03_remove_product_item_price(self):
        self.enable_environment("website_sale_no_sale.hide_price")
        self.disable_conflict_module("website_sale_add_to_cart.product")
        url = "/shop/product/ipod-20"
        code = """
                    if ($('b[data-oe-expression="product.website_price"]').length > 0) {
                        console.log('error', 'Price is not removed');
                    } else {
                        console.log('ok');
                    }
        """
        self.phantom_js(url, code, login="demo", ready="$('#product_details')")
