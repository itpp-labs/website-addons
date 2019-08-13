/*  Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
    # License MIT (https://opensource.org/licenses/MIT).*/
odoo.define("portal_event_tickets.ticket_change_tour", function(require) {
    "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    var options = {
        // Test: true,
        url: "/my/tickets",
        wait_for: base.ready(),
    };

    var tour_name = "ticket_change";
    tour.register(tour_name, options, [
        {
            content: "Click on a ticket",
            trigger: ".table-tickets .ticket-id",
        },
        {
            content: "Click [Change / Upgrade Ticket] button",
            trigger: '[data-target="#changeTicketModal"]',
        },
        {
            content: "Read warning and click [Continue]",
            trigger: ".btn-primary",
            extra_trigger: "#changeTicketModal",
        },
        // The user is redirected to event page.
        {
            content: "Select 1 ticket, which is more expensive than previous",
            // Extra_trigger: '#wrap:not(:has(a[href*="/event"]:contains("Conference on Business Apps")))',
            trigger: "select:eq(1)",
            run: "text 1",
        },
        {
            content: "Click on `Register Now` button",
            extra_trigger: "select:eq(1):has(option:contains(1):propSelected)",
            trigger:
                '.btn-primary:contains("Register Now"),.btn-primary:contains("Order Now")',
        },
        {
            content: "Fill attendees details",
            extra_trigger: "input[name='1-function']",
            trigger: "input[name='1-name']",
            run: function() {
                $("input[name='1-name']").val("Att1");
                $("input[name='1-phone']").val("111 111");
                $("input[name='1-email']").val("att1@example.com");
                $("select[name='1-country_id']").val("1");
                $("input[name='1-function']").val("JOB1");
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
                "h3:contains(We are glad to confirm your registration to our event),#step10",
            run: function() {
                // It's needed to don't make a click on the link
            },
        },

        // Next step to pay or confirm Sale Order in backend, which cannot be done via tour
    ]);
});
