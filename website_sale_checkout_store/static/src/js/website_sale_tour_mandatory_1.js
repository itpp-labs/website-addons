odoo.define('website_sale_checkout_store.tour', function (require) {
'use strict';

var tour = require("web_tour.tour");
var base = require("web_editor.base");

tour.register('shop_mandatory_fields_nobill_noship', {
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
            content: "select payment",
            trigger: 'a[id="nobill_noship"]',
        },
        {
            content: "filling in name",
            trigger: '.div_name input[name="name"]',
            run: "text name",
        },
        {
            content: "filling in email",
            trigger: '#div_email input[name="email"]',
            run: "text email@email.mn",
        },
        {
            content: "filling in phone",
            trigger: '#div_phone input[name="phone"]',
            run: "text 1234567890",
        },
        {
            content: "Confirm checkout",
            trigger: 'a:contains("Next")',
        },
        {
            content: "Confirm checkout",
            extra_trigger: 'h2:contains(Thank you for your order)',
            trigger: 'h2:contains(Thank you for your order)',
        },
    ]
);
});
