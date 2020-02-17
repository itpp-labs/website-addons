/* Copyright 2017 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
   Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
   License MIT (https://opensource.org/licenses/MIT). */
odoo.define("website_sale_checkout_store.tour.2", function(require) {
    "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    tour.register(
        "shop_mandatory_fields_bill_noship",
        {
            test: true,
            url: "/shop",
            wait_for: base.ready(),
        },
        [
            // For unsigned user
            {
                content: "search customizable desk",
                trigger: 'form input[name="search"]',
                run: "text customizable desk",
            },
            {
                content: "search customizable desk",
                trigger: 'form:has(input[name="search"]) .oe_search_button',
            },
            {
                content: "select desk customizable",
                extra_trigger: '.oe_product_cart a:contains("Customizable Desk")',
                trigger: '.oe_product_cart a:contains("Customizable Desk")',
            },
            {
                content: "click on add to cart",
                trigger: "#add_to_cart",
            },
            {
                content: "click on proceed to checkout",
                trigger: '.btn-primary span:contains("Proceed to Checkout")',
            },
            // --------------------------DEFAULT PART ENDS--------------------------------------
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
                trigger: "#country_id",
                run: "text 6",
            },
            {
                content: "Confirm checkout",
                trigger: 'a:contains("Next")',
            },
            {
                content: "click pay now",
                trigger: "button[type=submit]",
            },
            {
                content: "Confirm payment method",
                trigger: "td:contains('Wire Transfer')",
            },
            {
                content: "Confirm delivery method",
                trigger: "td:contains('Pickup at store')",
            },
        ]
    );
});
