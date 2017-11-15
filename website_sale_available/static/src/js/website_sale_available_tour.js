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
            content: "search iPad Retina",
            trigger: 'form input[name="search"]',
            run: "text iPad Retina",
        },
        {
            content: "search iPad Retina",
            trigger: 'form:has(input[name="search"]) .oe_search_button',
        },
        {
            content: "select iPad Retina",
            extra_trigger: '.oe_product_cart a:contains("iPad Retina")',
            trigger: '.oe_product_cart a:contains("iPad Retina")',
        },
        {
            content: "click on add to cart",
            trigger: '#product_detail form[action^="/shop/cart/update"] .btn',
        },
        {
            content: "Process Checkout",
            trigger: 'a.pull-right span.hidden-xs',
        },
        {
            content: "Warning block",
            extra_trigger: 'tr.warning',
            trigger: 'tr.warning',
        },
    ]
);
});
