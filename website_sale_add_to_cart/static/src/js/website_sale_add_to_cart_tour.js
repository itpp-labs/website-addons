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
            content: "search Apple Wireless Keyboard",
            trigger: 'form input[name="search"]',
            run: "text Apple Wireless Keyboard",
        },
        {
            content: "search Apple Wireless Keyboard",
            trigger: 'form:has(input[name="search"]) .oe_search_button',
        },
        {
            content: "add Apple Wireless Keyboard to cart",
            extra_trigger: '.oe_product_cart a:contains("Apple Wireless Keyboard")',
            trigger: '.float_left > .fa-plus',
        },
        {
            content: "click on add to cart",
            extra_trigger: '.my_cart_quantity',
            trigger: '.my_cart_quantity',
        },
        {
            content: "Process Checkout",
            trigger: $('a.pull-right span.hidden-xs'),
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
            trigger: 'h2:contains(Thank you for your order)',
        },
    ]
);
});
