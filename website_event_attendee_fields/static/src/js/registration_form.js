odoo.define('website_event_attendee_fields.registration_form', function (require) {

    var ajax = require('web.ajax');
    var core = require("web.core");

    var _t = core._t;


    var rows = {};
    function get_row($row){
        var counter = $row.attr('data-counter');
        var row = rows[counter];
        if (row){
            return row;
        }
        var $modal = $row.parent().parent().parent();
        row = {
            counter: counter,
            $row: $row,
            $modal: $modal,
            $submit: $modal.find('button[type="submit"]'),
            show_msg: function (msg, color){
                var $msg = $('<span/>').html(msg);
                if (color){
                    $msg.css('color', color);
                }
                this.$row.find('.message').html('').append($msg);
            },
            block: function(){
                this.$row.find('input,select').not('.email').attr('disabled', 1);
                this.$row.addClass('blocked');
                this.$submit.attr('disabled', '1');
            },
            disable_known_field: function(field){
                this.$row.find('[name=' + this.counter + '-' + field + ']').attr('disabled', 1);
            },
            reset: function(){
                // remove message and restrictions
                this.$row.find('input,select').removeAttr('disabled');
                this.$row.find('.message').html('');
                this.$row.removeClass('blocked');
                if (!this.$modal.find('.row.blocked').length){
                    this.$submit.removeAttr('disabled');
                }
            }
        };
        rows[counter] = row;
        return row;
    }

    function api_check_email(event_id, $row, email){
        return ajax.jsonRpc('/website_event_attendee_fields/check_email', 'call', {
            'event_id': event_id,
            'email': email,
        }).then(function(data){
            var row = get_row($row);
            if (data.email_not_allowed){
                row.show_msg(data.email_not_allowed, 'red');
                row.block();
            } else if (data.known_fields && data.known_fields.length){
                var msg = _t("This email address has already an account. Data will be taken from this account");
                row.show_msg(msg);
                _.each(data.known_fields, _.bind(row.disable_known_field, row));
            } else {
                row.reset();
            }
        });
    }

    function onchange_email(e, event_id){
        var $input = $(e.target);
        var email = $input.val();
        var $row = $input.parent().parent();
        return api_check_email(event_id, $row, email);
    }
    function init(){
        rows = {};
    }

    odoo.registration_form_init = init;
    odoo.registration_form_onchange_email = onchange_email;
});
