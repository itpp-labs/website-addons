/*  Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
    # License MIT (https://opensource.org/licenses/MIT).*/
odoo.define("portal_event_tickets.ticket_transfer_tour", function(require) {
    "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    var options = {
        // Test: true,
        url: "/my/tickets/transfer/receive",
        wait_for: base.ready(),
    };

    var tour_name = "ticket_transfer_receive";
    tour.register(tour_name, options, [
        {
            content: "Fill attendees details",
            extra_trigger: "input[name='1-function']",
            trigger: "input[name='1-name']",
            run: function() {
                // Fill:
                // * phone (optional)
                // * country_id (mandatory)
                // skip:
                // * job position (optional)
                $("input[name='1-phone']").val("111 111");
                $("select[name='1-country_id']").val("1");
            },
        },
        {
            content: "Validate attendees details",
            extra_trigger: "input[name='1-phone']",
            trigger: 'button:contains("Confirm")',
        },
        {
            content: "We are redirected to /my/tickets page",
            trigger: "h3:contains(Your Tickets)",
            run: function() {
                // It's needed to don't make a click on the link
            },
        },
    ]);
});
