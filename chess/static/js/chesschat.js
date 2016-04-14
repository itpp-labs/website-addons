//For odoo 8.0
//For odoo 8.0
(function() {
    "use strict";
    var ChessChat = openerp.ChessChat = {};
    ChessChat.COOKIE_NAME = 'chesschat_session';
    ChessChat.ConversationManager = openerp.Widget.extend({
        init: function (parent) {
            this._super(parent);
            console.log("Initial polling widget for chat");
            var self = this;
            // start the polling
            this.bus = openerp.bus.bus;
            this.bus.on("notification", this, this.on_notification);
            //this.bus.start_polling();
        },
        on_notification: function (notification) {
            console.log("on_notification")
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
             console.log("on_notification_do")
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
                $('.chat .user').seedColors(); //the random color
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
        init: function(parent){
            this._super(parent);
            var element = document.getElementById('chat')
			if (!element) {
				return;
			}
            this.c_manager = new openerp.ChessChat.ConversationManager(this);
            this.history = true;
            this.game_id = [];
            this.opening_chat = false;
            console.log("Initial chat");
        },
        start: function() {
            if (this.opening_chat) {
                return;
            }
            this.opening_chat = true;
            var self = this;
            var local_id = (location.href).split('/');
            var len_local_id = local_id.length;
            self.game_id = local_id[len_local_id-2];
            var cookie_name = ChessChat.COOKIE_NAME+self.game_id;
            //when game to finished is coockies is delete
            var cookie = openerp.get_cookie(cookie_name);
            var ready;
            if (!cookie) {
                console.log("Init and create coockie for chat");
                ready = openerp.jsonRpc("/chess/game/chat/init", "call", {game_id: self.game_id}).then(function (result) {
                    self.author_name = result.author_name; // current user
                    self.author_id = result.author_id;
                    self.game_id = result.game_id;
                    openerp.set_cookie(cookie_name, JSON.stringify({'game_id': self.game_id, 'author_name': self.author_name, 'author_id': self.author_id}), 30*24*60*60);
                });
            } else {
                console.log("Load history and coockie for chat");
                var game = JSON.parse(cookie);
                self.author_name = game.author_name; // current user
                self.author_id = game.author_id;
                self.game_id = game.game_id;
                ready = openerp.jsonRpc("/chess/game/chat/history", "call", {game_id: game.game_id}).then(function (history) {
                    if (history) {
                        self.load_history(history);
                    }
                    else{
                        console.log("Error. Not load history. (chat)");
                    }
                });
            }
            return ready;
        },
        load_history: function(history){
            if(this.history) {
                history.forEach(function (item, i, history) {
                    $(".chat #window_chat").append("<p><span class='user'>" + (item['author_name']) +
                        ":</span> " + (item['message']) + "<br> <span class='time_message'>" +
                        (item['date_message']) + "</span></p>");
                    $('.chat .user').seedColors(); //the random color current user
                    $(".chat #window_chat").each(function () {
                        this.scrollTop = this.scrollHeight;
                    });
                });
            };
            this.history=false;
        },
        send_message: function(message) {
            var self = this;
            openerp.jsonRpc("/chess/game/chat/send/", 'call', {message: message, game_id: self.game_id})
                .then(function (result) {
                    if(result) {
                        self.received_message(message);
                    } else {
                        console.log("error, message is not send");
                    }
                });
        },
        received_message: function (message) {
            var error = false;
            try {
                var date = new Date();
                var values = [date.getDate(), date.getMonth() + 1];
                for (var id in values) {
                    values[id] = values[id].toString().replace(/^([0-9])$/, '0$1');
                }
                var time_now = date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds();
                message.time = values[0] + '.' + values[1] + '.' + date.getFullYear() + ' ' + time_now;

                $(".chat #window_chat").append("<p><span class='user'>" + (message['author_name']) +
                    ":</span> " + (message['data']) + "<br> <span class='time_message'>" +
                    (message['time']) + "</span></p>");
                $('.chat .user').seedColors(); //the random color current user
                $(".chat #window_chat").each(function () {
                    this.scrollTop = this.scrollHeight;
                });

            } catch (err) {
                error = err;
                console.error(err);
            }
        },
        checked_chat: function(){
            if($("#toggle_chat").prop("checked")) {
                this.start();
            }
        },
        keydown: function(e) {
            if (e.keyCode == 13 && e.ctrlKey){
               this.select_message();
            }
        },
        click_send: function(){
            this.select_message();
        },
        select_message: function() {
            $('.chat .error').remove();
            var message = {};
            message.data = $(".chat #message_text").val();
            if (message.data == '' || message.data == ' ')
			{
				$('.chat #window_chat')
				.append('<div class="error">error: input message</div>');
				return false;
			}
            $('.chat #error').hide();
            $('.chat #message_text').val('');
            message.author_name = this.author_name;
            message.author_id = this.author_id;
            this.send_message(message);
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
    var my_chat = new ChessChat.Conversation();
    $(".toggle_chat").click(function(){
        my_chat.checked_chat(this);
    });

    $(".chat .message_btn").click(function(){
        my_chat.click_send(this);
    });
    $(".chat .message_text").keydown(function(e){
        my_chat.keydown(e);
    });
})();