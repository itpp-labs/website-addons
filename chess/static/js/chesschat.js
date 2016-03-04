odoo.define('chess.chesschat', function (require) {
    "use strict";

    var bus = require('bus.bus').bus;
    var session = require('web.session');
    var time = require('web.time');
    var utils = require('web.utils');
    var Widget = require('web.Widget');

    var ChessChat = {};

    ChessChat.ConversationManager = Widget.extend({
        init: function(parent) {
            var self = this;
            this._super(parent);
            this.message = [];
            this.game_id = false;
            this.start();
        },

        start: function(){
            var self = this;

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
            if(Array.isArray(channel) && channel[1] === 'chess'){
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
            "click .toggle_chat": "checked_chat",
        },

        init: function() {
            this.game = null;
            this.messages = [];
        },

        opening_chat: function() {
            if (this.opening_chat) {
                return;
            }
            this.opening_chat = true;

            var self = this;
            /*в кукки буду хранить ID игры,
            если игра уже была когда то загружена то мы показываем историю переписки
            если игра впервые то инициализируем переменные */
            var cookie = utils.get_cookie('chesschat_session');
            var ready;
            if (!cookie) {
            ready = session.rpc("/chess/game/chat/init", {game_id: self.chess.game.message_game_ids.game_id}).then(function (result) {
                self.author_name = result.author_name; // имя текущего игрока
                self.game_id = game_id;
                utils.set_cookie('chesschat_session', JSON.stringify(self.game_id), 60*60);
            });
            } else {
                var game = JSON.parse(cookie);
                ready = session.rpc("/chess/game/chat/history", {game_id: game.id, limit: 100}).then(function (history) {
                    self.history = history;
                });
            }
            ready.always(function () {
                self.opening_chat = false;
            });

            return ready;
        },


        start: function(){
            if (this.history) {
                console.log("load history");
                //show_history()
            }
        },

        /*show_history:function(){

        },*/

        checked_chat: function(){
            if($("#toggle_chat").prop("checked")) {
                opening_chat();
            } else {
                console.log("chat is not open");
            }
        };

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
        },

        send_message: function(message) {
            console.log('send message', message);
            var self = this;
            var send_it = function() {
                return session.rpc("/chess/game/chat/send/", {game_id: self.chess.game.message_game_ids.game_id, message: message});
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

        keydown: function(e) {
            if (e.keyCode == 13 && e.ctrlKey){
                select_message();
            }
        },

        click_send: function(){
            select_message();
        },

        select_message: function() {
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

    return ChessChat;
});