odoo.define('website_sale_add_to_cart.tour', function (require) {
'use strict';

var tour = require("web_tour.tour");
var base = require("web_editor.base");

tour.register('shop_add_to_cart', {
    test: true,
    url: '/shop',
    wait_for: base.ready()
},
    [
        // for unsigned user
        {
            content: "search iMac",
            trigger: 'form input[name="search"]',
            run: "text iMac",
        },
        {
            content: "search iMac",
            trigger: 'form:has(input[name="search"]) .oe_search_button',
        },
        {
            content: "add iMac to cart",
            extra_trigger: '.oe_product_cart a:contains("iMac")',
            trigger: '.float_left > .fa-plus',
        },
        {
            content: "click on add to cart",
            extra_trigger: '.my_cart_quantity',
            trigger: '.my_cart_quantity',
        },
        {
            content: "Process Checkout",
            trigger: 'span:contains("Process Checkout")',
        },
        {
            content: "Confirm checkout",
            trigger: 'a:contains("Confirm")',
        },
        {
            content: "pay now",
            trigger: 'button:contains("Pay Now")',
        },
        {
            content: "Confirm checkout",
            extra_trigger: 'h2:contains(Thank you for your order)',
            trigger: 'a[href="/shop/print"]',
        },
    ]
);
});
