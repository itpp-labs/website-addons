/* Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
   License MIT (https://opensource.org/licenses/MIT). */
odoo.define("website_multi_company.web_editor.tour", function(require) {
    "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    var options = {
        test: true,
        url: "/?debug",
        wait_for: base.ready(),
    };

    var tour_name = "website_multi_company.web_editor.tour";
    tour.register(tour_name, options, [
        {
            content: "Click Customize",
            trigger: "#customize-menu>a",
        },
        {
            content: "Click HTML/CSS Editor",
            trigger: "#html_editor>a",
        },
        // Multi-website
        {
            content: "Click Search Box",
            trigger: "#s2id_ace-view-list>a",
        },
        {
            content: "Select Some Multi-Website view",
            trigger: "#select2-drop li:contains(Website #)",
        },
        {
            content: 'Ok, let\'s check that button "Make Multi-Website" is not visible',
            trigger: ".ace_content",
            run: function(actions) {
                if ($('[data-action="make-multi-website"]:visible').length) {
                    console.error("Make Multi-Website must not be visible");
                }
            },
        },
        // Non Multi-website
        {
            content: "Click Search Box",
            trigger: "#s2id_ace-view-list>a",
        },
        {
            content: "Select Some Non Multi-Website view",
            trigger: "#select2-drop li:not(:has(div:contains(Website #))",
        },
        {
            content: 'Ok, let\'s check that button "Make Multi-Website" is visible',
            trigger: ".ace_content",
            run: function(actions) {
                if (!$('[data-action="make-multi-website"]:visible').length) {
                    console.error("Make Multi-Website must be visible");
                }
            },
        },
    ]);
});
