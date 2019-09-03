odoo.define('website_sale_search_tags.tour', function (require) {
'use strict';

var tour = require("web_tour.tour");
var base = require("web_editor.base");

tour.register('website_sale_search_tags', {
    test: true,
    url: '/shop',
    wait_for: base.ready()
},
    [
        // for unsigned user
        {
            content: "type to search Apple Wireless Keyboard",
            trigger: 'form input[name="search"]',
            run: "text Apple Wireless Keyboard",
        },
        {
            content: "search Apple Wireless Keyboard",
            trigger: 'form:has(input[name="search"]) .oe_search_button',
        },
        {
            content: "make sure that Apple Wireless Keyboard is founded and type to search iMac",
            extra_trigger: '.oe_product_cart:eq(0) a:contains("Apple Wireless Keyboard")',
            trigger: 'form input[name="search"]',
            run: "text iMac",
        },
        {
            content: "search iMac",
            trigger: 'form:has(input[name="search"]) .oe_search_button',
        },
        {
            content: "make sure that iMac is founded",
            extra_trigger: '.oe_product_cart:eq(0) a:contains("iMac")',
            trigger: 'form input[name="search"]',
            run: "text OK!",
        }
    ]
);
});
