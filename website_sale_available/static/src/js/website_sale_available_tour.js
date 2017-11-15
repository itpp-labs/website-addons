odoo.define('website_sale_available.tour', function (require) {
'use strict';

var tour = require("web_tour.tour");
var base = require("web_editor.base");

tour.register('shop_sale_available', {
    test: true,
    url: '/shop',
    wait_for: base.ready()
},
    [
        // for unsigned user
        {
            content: "search ipod",
            trigger: 'form input[name="search"]',
            run: "text ipod",
        },
        {
            content: "search ipod",
            trigger: 'form:has(input[name="search"]) .oe_search_button',
        },
        {
            content: "select ipod",
            extra_trigger: '.oe_product_cart a:contains("iPod")',
            trigger: '.oe_product_cart a:contains("iPod")',
        },
        {
            content: "click on add to cart",
            trigger: '#product_detail form[action^="/shop/cart/update"] .btn',
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
