odoo.define('website_event_attendee_fields.test_tour', function (require) {
'use strict';

    var tour = require('web_tour.tour');
    var base = require("web_editor.base");

    tour.register('website_event_attendee_fields_test_tour_base', {
        test: true,
        url: '/event',
        wait_for: base.ready()
    }, [

        {
            content: "Go to the `Events` page",
            trigger: 'a[href*="/event"]:contains("Conference on Business Apps"):first',
        },
        {
            content: "Select 1 unit of `Standard` ticket type",
            extra_trigger: '#wrap:not(:has(a[href*="/event"]:contains("Conference on Business Apps")))',
            trigger: 'select:eq(0)',
            run: 'text 1',
        },
        {
            content: "Select 2 units of `VIP` ticket type",
            extra_trigger: 'select:eq(0):has(option:contains(1):propSelected)',
            trigger: 'select:eq(1)',
            run: 'text 2',
        },
        {
            content: "Click on `Order Now` button",
            extra_trigger: 'select:eq(1):has(option:contains(2):propSelected)',
            trigger: '.btn-primary:contains("Order Now")',
        },
        {
            content: "Fill attendees details",
            trigger: 'form[id="attendee_registration"] .btn:contains("Continue")',
            run: function () {
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

                $("input[name='3-name']").val("Att3");
                $("input[name='3-phone']").val("333 333");
                $("input[name='3-email']").val("att3@example.com");
                $("select[name='3-country_id']").val("1");
                $("input[name='3-function']").val("JOB3");
            }
        },
        {
            content: "Validate attendees details",
            extra_trigger: "input[name='1-name'], input[name='2-name'], input[name='3-name']",
            trigger: 'button:contains("Continue")',
        },

    ]);


});
