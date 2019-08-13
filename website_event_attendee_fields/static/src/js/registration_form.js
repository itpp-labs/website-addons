/*  Copyright 2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
    # License MIT (https://opensource.org/licenses/MIT).*/
odoo.define("website_event_attendee_fields.registration_form", function(require) {
    "use strict";
    var ajax = require("web.ajax");
    var core = require("web.core");
    var website_event = require("website_event.website_event");

    var _t = core._t;

    website_event.EventRegistrationForm.include({
        on_click: function(ev) {
            // Remove old form which is only hidden, but still presents in dom when user close popup and then click Register (Order) again
            $("#modal_attendees_registration").remove();
            return this._super.apply(this, arguments);
        },
    });

    var rows = {};
    function get_row($row) {
        var counter = $row.attr("data-counter");
        var row = rows[counter];
        if (row) {
            return row;
        }
        var $modal = $row
            .parent()
            .parent()
            .parent();
        row = {
            counter: counter,
            $row: $row,
            $modal: $modal,
            $submit: $modal.find('button[type="submit"]'),
            get_email: function() {
                return $.trim(this.$row.find(".email").val());
            },
            show_msg: function(msg, color) {
                var $msg = $("<span/>").html(msg);
                if (color) {
                    $msg.css("color", color);
                }
                this.$row
                    .find(".message")
                    .html("")
                    .append($msg);
            },
            block: function() {
                this.$row
                    .find("input,select")
                    .not(".email")
                    .attr("disabled", 1);
                this.$row.addClass("blocked");
                this.$submit.attr("disabled", "1");
            },
            disable_known_field: function(field) {
                this.$row
                    .find("[name=" + this.counter + "-" + field + "]")
                    .attr("disabled", 1);
            },
            reset: function() {
                // Remove message and restrictions
                this.$row.find("input,select").removeAttr("disabled");
                this.$row.find(".message").html("");
                this.$row.removeClass("blocked");
                if (!this.$modal.find(".row.blocked").length) {
                    this.$submit.removeAttr("disabled");
                }
            },
        };
        rows[counter] = row;
        return row;
    }

    function api_check_email(event_id, $row) {
        // Check form
        var row = get_row($row);
        var email = row.get_email();
        var has_duplicate = _.some(rows, function(r) {
            if (r.counter === row.counter) {
                // Don't compare with itself
                return false;
            }
            if (email !== r.get_email()) {
                // Emails are different
                return false;
            }
            var msg = _t("Sorry, but each attendee has to have unique email.");
            row.show_msg(msg);
            row.block();

            return true;
        });

        if (has_duplicate) {
            // Already have an error. No need to ask backend.
            return $.when();
        }

        // Check backend
        return ajax
            .jsonRpc("/website_event_attendee_fields/check_email", "call", {
                event_id: event_id,
                email: email,
            })
            .then(function(data) {
                if (data.email_not_allowed) {
                    row.show_msg(data.email_not_allowed, "red");
                    row.block();
                } else if (data.known_fields && data.known_fields.length) {
                    var msg = _t(
                        "This email address has already an account. Data will be taken from this account"
                    );
                    row.show_msg(msg);
                    _.each(data.known_fields, _.bind(row.disable_known_field, row));
                } else {
                    row.reset();
                }
            });
    }

    function onchange_email(input, event_id) {
        var $input = $(input);
        var $row = $input.parent().parent();
        return api_check_email(event_id, $row);
    }
    function init() {
        rows = {};
    }

    odoo.registration_form_init = init;
    odoo.registration_form_onchange_email = onchange_email;
});
