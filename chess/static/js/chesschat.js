//For odoo 8.0
(function() {
    "use strict";
    var ChessChat = openerp.ChessChat = {};
    ChessChat.COOKIE_NAME = 'chesschat_session';

    ChessChat.ConversationManager = openerp.Widget.extend({
        init: function (parent) {
            var self = this;
            this._super(parent);
            this.message = [];
            this.game_id = false;
            this.game = null;
            this.start();
        },
        start: function () {
            var self = this;
            // start the polling
            this.bus = openerp.bus.bus;
            this.bus.on("notification", this, this.on_notification);
            this.bus.start_polling();
        },
        on_notification: function (notification) {
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
            if (Array.isArray(channel) && channel[1] === 'chess.game.chat') {
                try {
                    this.received_message();
                } catch (err) {
                    error = err;
                    console.error(err);
                }
            }
        },
        received_message: function(message) {
            var error = false;
            try {
                console.log('received message');

                var date = new Date();
                var values = [date.getDate(), date.getMonth() + 1];
                for (var id in values) {
                    values[id] = values[id].toString().replace(/^([0-9])$/, '0$1');
                }
                var time_now = date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds();
                message.time = values[0] + '.' + values[1] + '.' + date.getFullYear() + ' ' + time_now;

                $("#window_chat").append("<p><span class='user'>" + (message['author_name']) +
                    "</span>: " + (message['data']) + "<br> <span class='time_message'>" +
                    (message['time']) + "</span></p>");
                $("#window_chat").each(function () {
                    this.scrollTop = this.scrollHeight;
                });

            } catch (err) {
                error = err;
                console.error(err);
            }
        }
    });

    ChessChat.Conversation = openerp.Widget.extend({
        className: "chat_form",
        events: {
            "click .toggle_chat": "checked_chat",
            "keydown .message_text": "keydown",
            "click .message_btn": "click_send",
        },
        init: function(){
            this.c_manager = new openerp.ChessChat.ConversationManager(this);
        },
        opening_chat: function() {
            console.log("opening chat");
            if (this.opening_chat) {
                return;
            }
            this.opening_chat = true;
            var self = this;

            var cookie = openerp.get_cookie(ChessChat.COOKIE_NAME);
            var ready;

            if (!cookie) {
            ready = openerp.session.rpc("/chess/game/chat/init", {game_id: self.chess.game.message_game_ids.game_id}).then(function (result) {
                self.author_name = result.author_name; // current user
                self.game_id = result.game_id;
                openerp.set_cookie(ChessChat.COOKIE_NAME, JSON.stringify({'game_id': self.game_id, 'author_name': author_name}), 60*60);
            });
            } else {
                var game = JSON.parse(cookie);
                ready = openerp.session.rpc("/chess/game/chat/history", {game_id: game.game_id, limit: 100}).then(function (history) {
                    self.history = history;
                });
                self.author_name = game.author_name // current user
            }
            ready.always(function () {
                self.opening_chat = false;
            });

            return ready;
        },
        load_history: function(){
            if (this.history) {
                console.log("load history");
                var history = this.history
                history.forEach(function(item, i, history) {
                    $("#window_chat").append("<p><span class='user'>" + (item['author_name']) +
                        "</span>: " + (item['message']) + "<br> <span class='time_message'>" +
                        (item['date_message']) + "</span></p>");
                    $("#window_chat").each(function () {
                        this.scrollTop = this.scrollHeight;
			        });
                });
            }
        },
        checked_chat: function(){
            if($("#toggle_chat").prop("checked")) {
                opening_chat();
            } else {
                console.log("chat is not open");
            }
        },
        send_message: function(message) {
            console.log('send message', message);
            var self = this;
            var send_it = function() {
                return openerp.session.rpc("/chess/game/chat/send/", {game_id: self.chess.game.message_game_ids.game_id, message: message});
            };
            var tries = 0;
            send_it().fail(function(error, e) {
                e.preventDefault();
                tries += 1;
                if (tries < 3)
                    return send_it();
            });
            send_it().then(function(){
                received_message(message);
            });
        },
        received_message: function (message) {
            var error = false;
            try {
                console.log('received message');

                var date = new Date();
                var values = [date.getDate(), date.getMonth() + 1];
                for (var id in values) {
                    values[id] = values[id].toString().replace(/^([0-9])$/, '0$1');
                }
                var time_now = date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds();
                message.time = values[0] + '.' + values[1] + '.' + date.getFullYear() + ' ' + time_now;

                $("#window_chat").append("<p><span class='user'>" + (message['author_name']) +
                    "</span>: " + (message['data']) + "<br> <span class='time_message'>" +
                    (message['time']) + "</span></p>");
                $("#window_chat").each(function () {
                    this.scrollTop = this.scrollHeight;
                });

            } catch (err) {
                error = err;
                console.error(err);
            }
        },
        keydown: function(e) {
            console.log("keydown");
            if (e.keyCode == 13 && e.ctrlKey){
                select_message();
            }
        },
        click_send: function(){
            console.log("click_send");
            select_message();
        },
        select_message: function() {
            console.log("select_message");
            $('.error').remove();
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
            message.author_name = this.author_name;
            send_message(message);
        }
    });

    openerp.set_cookie = function(name, value, ttl) {
        ttl = ttl || 24*60*60*365;
        document.cookie = [
            name + '=' + value,
            'path=/',
            'max-age=' + ttl,
            'expires=' + new Date(new Date().getTime() + ttl*1000).toGMTString()
        ].join(';');
    };
    return ChessChat;
})();
