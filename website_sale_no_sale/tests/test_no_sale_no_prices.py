# Copyright 2018 Denis Mudarisov <https://it-projects.info/team/trojikman>
# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import odoo.tests


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):
    def enable_environment(self, template_id):
        self.env['ir.ui.view'].search([('active', '=', False), ('key', '=', template_id)]).write({'active': True})

    def disable_conflict_module(self, template_id):
        custom_website_view = self.env['ir.ui.view'].search([('active', '=', True), ('key', '=', template_id)])
        if custom_website_view:
            custom_website_view.write({'active': False})

    def test_01_remove_products_prices(self):
        self.enable_environment('website_sale_no_sale.hide_products_prices')
        url = '/shop'
        code = """
                    if ($('.oe_currency_value').length > 0) {
                        console.log(document.documentElement.innerHTML);
                        console.log('error', 'Prices is not removed');
                    } else {
                        console.log('ok');
                    }
        """
        self.phantom_js(url, code, "odoo.__DEBUG__.services['web_tour.tour'].tours.shop.ready", login="demo")

    def test_02_remove_add_to_cart(self):
        self.enable_environment('website_sale_no_sale.hide_add_to_cart')
        self.disable_conflict_module('website_sale_add_to_cart.product')
        url = '/shop/product/customizable-desk-9'
        code = """
                    if ($('#add_to_cart').hasClass('o_hidden')) {
                        console.log('ok');
                    } else {
                        console.log(document.documentElement.innerHTML);
                        console.log('error', 'Add to cart button is not removed');
                    }
        """
        self.phantom_js(url, code, "odoo.__DEBUG__.services['web_tour.tour'].tours.shop.ready", login="demo")

    def test_03_remove_product_item_price(self):
        self.enable_environment('website_sale_no_sale.hide_price')
        self.disable_conflict_module('website_sale_add_to_cart.product')
        url = '/shop/product/customizable-desk-9'
        code = """
                    if ($('b.oe_price span.oe_currency_value').length > 0) {
                        console.log(document.documentElement.innerHTML);
                        console.log('error', 'Price is not removed');
                    } else {
                        console.log('ok');
                    }
        """
        self.phantom_js(url, code, "odoo.__DEBUG__.services['web_tour.tour'].tours.shop.ready", login="demo")
