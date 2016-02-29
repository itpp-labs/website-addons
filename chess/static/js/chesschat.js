odoo.define('chess.chesschat', function (require) {
    "use strict";

    var core = require('web.core');
    var bus = require('bus.bus');
    var session = require('web.session');
    var models = require('chess.models');
    var Widget = require('web.Widget');

    var NBR_LIMIT_HISTORY = 20;

    var _t = core._t;
    var ChessChat = {};

    ChessChat.ConversationManager = Widget.extend({
        init: function() {
            var self = this;
            this.message = [];

            //bus
            this.bus = bus.bus;
            this.bus.on("notification", this, this.on_notification);
            this.bus.start_polling();
        },

        on_notification: function(notification) {
            var self = this;
            if (typeof notification[0][0] === 'string') {
                notification = [notification]
            }
            for (var i = 0; i < notification.length; i++) {
                var channel = notification[i][0];
                var message = notification[i][1];
                this.on_notification_do(channel, message);
            }
        },

        on_notification_do: function (channel, message) {
            var error = false;
            if(Array.isArray(channel) && channel[1] === '??????session?????'){
                try{
                    this.received_message(message);
                }catch(err){
                    error = err;
                    console.error(err);
                }
            }
        },

        received_message: function(message) {
            var error = false;
            try{
                console.log('received message');

                var date = new Date();
                var values = [ date.getDate(), date.getMonth() + 1 ];
                for(var id in values){
                    values[id] =values[id].toString().replace(/^([0-9])$/,'0$1');
                }
                var time_now = date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds();
                message.time = values[0] + '.' + values[1] + '.' + date.getFullYear() + ' ' + time_now;

                $("#window_chat").append("<p><span class='user'>" + (message['author_name']) +
				    "</span>: " + (message['data']) + "<br> <span class='time_message'>" +
				    (message['time']) + "</span></p>");
			    $("#window_chat").each(function () {
				    this.scrollTop = this.scrollHeight;
			    });

            }catch(err){
                error = err;
                console.error(err);
            }
        }
    });


    ChessChat.Conversation = Widget.extend({
        className: "chat_form",

        events: {
            "keydown .message_text": "keydown",
            "click .message_btn": "click_send",
        },

        init: function(parent, c_manager, session, options) {
            this._super(parent);
            this.c_manager = c_manager;
            this.options = options || {};
            this.loading_history = true;
            this.set("messages", []);

        },

        start: function() {
            var self = this;
            //self.load_history();
        },

       /* load_history: function(){
            var self = this;
            if(this.loading_history){
                var data = {game_id: self.chess.game.message_game_ids.game_id, limit: NBR_LIMIT_HISTORY};
                session.rpc("/chess/game/load_history/", data)
                    .then(function(message){
                    if(message){
                        self.insert_history(message);
    					if(messages.length != NBR_LIMIT_HISTORY){
                            self.loading_history = false;
                        }
                    }else{
                        self.loading_history = false;
                    }
                });
            }
        },

        insert_history: function(message) {
            /*show message*/
       // },

        send_message: function(message) {
            console.log('send message', message);
            var self = this;
            var send_it = function() {
                return session.rpc("/chess/game/send/", {game_id: self.chess.game.message_game_ids.game_id, message: message});
            };
            var tries = 0;
            send_it().fail(function(error, e) {
                e.preventDefault();
                tries += 1;
                if (tries < 3)
                    return send_it();
            });
        },

        keydown: function(e) {
            if (e.keyCode == 13 && e.ctrlKey){
                select_message();
            }
        },

        click_send: function(){
            select_message();
        },

        select_message: function() {
            $('.error').remove(); //clear errors
            var message = [];
            message.data = $("#message_text").val();
            if (message.data == '' || message.data == ' ')
			{
				$('#window_chat')
				.append('<div class="error">error: input message</div>');
				return false;
			}
            $('#error').hide();
            $('#message_text').val('');
            send_message(message);
        }
    });

    return ChessChat;
});