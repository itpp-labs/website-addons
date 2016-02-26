odoo.define('chess.chesschat', function (require) {
    "use strict";

    var data = {};

    var bus = require('bus.bus').bus;
    var session = require('web.session');
    var models = require('chess.models');

    var ChessChat = {};


    ChessChat = {

        init: function () {
            $('.error').remove(); //clear errors
            data.message = $("#message_text").val();
            if (data.message == '' || data.message == ' ')
			{
				$('#window_chat')
				.append('<div class="error">error: input message</div>');
				return false;
			}
			$('#error').hide();
			data.user = 'Dinar'; //for example
			data.time = '26.02.2016'; //for example
			$('#message_text').val('');

            console.log('click send message');
            this.send_message(data);
        },

        send_message: function(data) {
            console.log('send', data);
            var self = this;
            var send_it = function() {
                return session.rpc("/chess/game/send/", {game_id: self.chess.game.message_game_ids.game_id, message: data});
            };
            //game_id it's correctly?

            var tries = 0;
            send_it().fail(function(error, e) {
                e.preventDefault();
                tries += 1;
                if (tries < 3)
                    return send_it();
            });
        },

        get_message: function(data) {

            console.log('get message');
            console.log(data['message']);

            $("#window_chat").append("<p><span class='user'>" + (data['user']) +
				"</span>: " + (data['message']) + "<br> <span class='time_message'>" +
				(data['time']) + "</span></p>");

			$("#window_chat").each(function () {
				this.scrollTop = this.scrollHeight;
			});

        },


        on_notification: function(notification) {
            var self = this;
            var channel = notification[0];
            var message = notification[1];

            this.pos.db.save('bus_last', this.bus.last)
        }
    };

    return ChessChat;
});