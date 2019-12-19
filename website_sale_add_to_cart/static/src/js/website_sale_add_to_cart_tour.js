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
            extra_trigger: '.oe_product_cart:eq(0) a:contains("Apple Wireless Keyboard")',
            trigger: '.quick_add_to_cart input',
            run: "text 1",
        },
        {
            content: "add one more",
            trigger: '.float_left > .fa-plus',
        },
        {
            content: "load product page to increase coverage",
            trigger: 'a:contains("Apple Wireless Keyboard")',
        },
        {
            content: "add one more",
            extra_trigger: 'input[name="add_qty"]',
            trigger: '.float_left > .fa-plus',
        },
        {
            content: "return back",
            trigger: 'form:has(input[name="search"]) .oe_search_button',
        },
        {
            content: "add Apple Wireless Keyboard to cart",
            extra_trigger: '.oe_product_cart a:contains("Apple Wireless Keyboard")',
            trigger: 'i.fa.fa-minus',
        },
        {
            content: "check product presence",
            extra_trigger: '.my_cart_quantity',
            trigger: '.my_cart_quantity',
        },
        {
            content: "check quantity",
            extra_trigger: 'input[value="2"]',
            trigger: 'th:contains(Price)',
        },
    ]
);
});
