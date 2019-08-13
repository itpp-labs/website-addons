/*  Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
    # License MIT (https://opensource.org/licenses/MIT).*/
odoo.define("website_event_attendee_fields.test_tour", function(require) {
    "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    tour.register(
        "website_event_attendee_fields_test_tour_base",
        {
            test: true,
            url: "/event",
            wait_for: base.ready(),
        },
        [
            {
                content: "Go to the `Events` page",
                trigger:
                    'a[href*="/event"]:contains("Conference on Business Apps"):first',
            },
            {
                content: "Select 2 unit of 'Free Ticket'",
                extra_trigger:
                    '#wrap:not(:has(a[href*="/event"]:contains("Conference on Business Apps")))',
                trigger: "select:eq(0)",
                run: "text 2",
            },
            {
                content: "Click on `Register Now` button",
                extra_trigger: "select:eq(0):has(option:contains(2):propSelected)",
                trigger:
                    '.btn-primary:contains("Register Now"),.btn-primary:contains("Order Now")',
            },
            {
                content: "Fill attendees details",
                extra_trigger: "input[name='1-function']",
                trigger: "input[name='1-name']",
                run: function() {
                    if ($("input[name='2-email']").val()) {
                        console.log("error", "Only first attendee can be autofilled");
                    }
                    $("input[name='1-name']").val("Att1");
                    $("input[name='1-phone']").val("111 111");
                    $("input[name='1-email']").val("att1@example.com");
                    $("select[name='1-country_id']").val("1");
                    $("input[name='1-function']").val("JOB1");

                    $("input[name='2-name']").val("Att2");
                    $("input[name='2-phone']").val("222 222");
                    $("input[name='2-email']").val("att2@example.com");
                    $("select[name='2-country_id']").val("1");
                    $("input[name='2-function']").val("JOB2");
                },
            },
            {
                content: "Validate attendees details",
                extra_trigger: "input[name='1-name'], input[name='2-name']",
                trigger: 'button:contains("Continue")',
            },
            {
                content: "Dummy step to finish loadding of previous step",
                trigger:
                    "h3:contains(We are glad to confirm your registration to our event),a:contains(Return to Cart),h3:contains(Your Address),span:contains(Continue Shopping)",
                run: function() {
                    // It's needed to don't make a click on the link
                },
            },
        ]
    );
});
