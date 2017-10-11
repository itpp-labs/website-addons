odoo.define('website_sale.tour', function (require) {
'use strict';

var tour = require("web_tour.tour");
var base = require("web_editor.base");

tour.register('shop_buy_product', {
    test: true,
    url: '/shop',
    wait_for: base.ready()
},
    [
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
            content: "select ipod 32GB",
            extra_trigger: '#product_detail',
            trigger: 'label:contains(32 GB) input',
        },
        {
            content: "click on add to cart",
            extra_trigger: 'label:contains(32 GB) input:propChecked',
            trigger: '#product_detail form[action^="/shop/cart/update"] .btn',
        },
        //--------------------------DEFAULT PART ENDS--------------------------------------
        {
            content: "select payment",
            trigger: 'a[id="nobill_noship"]',
        },
        {
            content: "filling in",
            trigger: '.div_name input:contains[name="name"] input',
            run: "text name",
        },
        {
            content: "filling in",
            trigger: '#div_email input:contains[name="email"] input',
            run: "text email@email.mn",
        },
        {
            content: "filling in",
            trigger: '#div_phone input:contains[name="phone"] input',
            run: "text 1234567890",
        },
        {
            content: "Confirm checkout",
            trigger: 'a:contains("Next")',
        },
    ]
);

});
