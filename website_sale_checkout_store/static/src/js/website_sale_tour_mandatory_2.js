odoo.define('website_sale_checkout_store.tour', function (require) {
'use strict';

var tour = require("web_tour.tour");
var base = require("web_editor.base");

tour.register('shop_mandatory_fields_bill_noship', {
    test: true,
    url: '/shop',
    wait_for: base.ready()
},
    [
        {
            content: "log out dropdown",
            trigger: '#top_menu a[href="#"]',
        },
        {
            content: "log out",
            trigger: '#o_logout a[href="/web/session/logout?redirect=/"]',
        },
        {
            content: "log out",
            trigger: 'a[href="/shop"]',
        },
        // further for unsigned user
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
            trigger: '.oe_product_cart a:contains("iPod")',
        },
        {
            content: "click on add to cart",
            trigger: '#product_detail form[action^="/shop/cart/update"] .btn',
        },
        //--------------------------DEFAULT PART ENDS--------------------------------------
        {
            content: "select payment",
            trigger: 'a[id="bill_noship"]',
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
            content: "filling in a country",
            trigger: '#country_id',
            run: 'text 6',
        },
        {
            content: "Confirm checkout",
            trigger: 'a:contains("Next")',
        },
        {
            content: "click confirm",
            trigger: 'a[href="/shop/confirm_order"]',
        },
        {
            content: "click pay now",
            trigger: 'button[type=submit]',
        },
        {
            content: "Confirm checkout",
            extra_trigger: 'h2:contains(Thank you for your order)',
            trigger: 'a[href="/shop/print"]',
        },
    ]
);

});
