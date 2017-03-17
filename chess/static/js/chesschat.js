odoo.define('chess.chesschat', function (require) {
    "use strict";
    var Widget = require('web.Widget');
    var session = require('web.session');
    var set_cookie = require('chess.common');
    var utils = require('web.utils');
    var bus = require('bus.bus');
    var ChessChat = {};

    ChessChat.COOKIE_NAME = 'chesschat_session';
    ChessChat.Conversation = Widget.extend({
        className: "chat_form",
        init: function(model_game_id, dbname, uid){
            var element = document.getElementById('chat');
            if (!element) {
                return;
            }
            this.game_id = model_game_id;
            this.history = true;
            this.opening_chat = false;
        },

        on_notification: function (notification) {
            var self = this;
            for (var i = 0; i < notification.length; i++) {
                var channel = notification[i][0];
                var message = notification[i][1];
                this.on_notification_do(channel, message);
            }
        },

        on_notification_do: function (channel, message) {
            var channel = JSON.parse(channel);
            var error = false;
            if (Array.isArray(channel) && channel[1] === 'chess.game.chat') {
                try {
                    this.received_message(message);
                } catch (err) {
                    error = err;
                    console.error(err);
                }
            }
        },

        start: function() {
            if (this.opening_chat) {
                return;
            }
            this.opening_chat = true;
            var self = this;
            var cookie_name = ChessChat.COOKIE_NAME+self.game_id;
            //when game to finished is coockies is delete
            var cookie = utils.get_cookie(cookie_name);
            var ready;
            if (!cookie) {
                ready = session.rpc("/chess/game/chat/init", {game_id: self.game_id}).then(function (result) {
                    self.author_name = result.author_name; // current user
                    self.author_id = result.author_id;
                    self.game_id = result.game_id;
                    set_cookie(cookie_name, JSON.stringify({'game_id': self.game_id, 'author_name': self.author_name, 'author_id': self.author_id}), 30*24*60*60);
                });
            } else {
                var game = JSON.parse(cookie);
                self.author_name = game.author_name; // current user
                self.author_id = game.author_id;
                self.game_id = game.game_id;
                ready = session.rpc("/chess/game/chat/history", {game_id: game.game_id}).then(function (history) {
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
                    $(".chat #window_chat").append("<p><span class='user'>" + (item.author_name) +
                        ":</span> " + (item.message.replace(/&/gm,'&amp;').replace(/</gm,'&lt;').replace(/>/gm,'&gt;')) + "<br> <span class='time_message'>" +
                        (item.date_message) + "</span></p>");
                    $('.chat .user').seedColors(); //the random color current user
                    $(".chat #window_chat").each(function () {
                        this.scrollTop = this.scrollHeight;
                    });
                });
            }
            this.history=false;
        },
        send_message: function(message) {
            var self = this;
            return session
                .rpc("/chess/game/chat/send/", {message: message, game_id: self.game_id})
                .then(function (result) {
                    if(result) {
                        self.received_message(message);
                        console.log("Message is sent.");
                    } else {
                        console.log("Error. Message not sent.");
                        console.log("No response from the server.");
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

                $(".chat #window_chat").append("<p><span class='user'>" + (message.author_name) +
                    ":</span> " + (message.data.replace(/&/gm,'&amp;').replace(/</gm,'&lt;').replace(/>/gm,'&gt;')) + "<br> <span class='time_message'>" +
                    (message.time) + "</span></p>");
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
                .append('<div class="error"><span class="fa fa-times">ERROR. Input message.</span></div>');
                $(".chat #window_chat").each(function () {
                    this.scrollTop = this.scrollHeight;
                });
                return false;
            }
            $('.chat #error').hide();
            $('.chat #message_text').val('');
            message.author_name = this.author_name;
            message.author_id = this.author_id;
            this.send_message(message);
        }
    });
    set_cookie = function(name, value, ttl) {
        ttl = ttl || 24*60*60*365;
        document.cookie = [
            name + '=' + value,
            'path=/',
            'max-age=' + ttl,
            'expires=' + new Date(new Date().getTime() + ttl*1000).toGMTString()
        ].join(';');
    };
    $(document).ready(function() {
    if (window.model_game_id===undefined) {
        return false;
    } else {
         var my_chat = new ChessChat.Conversation(model_game_id, model_dbname, model_author_id);
    }

    $(".toggle_chat").click(function(){
        my_chat.checked_chat(this);
    });

    $(".chat .message_btn").click(function(){
        my_chat.click_send(this);
    });
    $(".chat .message_text").keydown(function(e){
        my_chat.keydown(e);
    });
        $("#chat_form").submit(function(event) {
        return false;
    });
    $("#toggler").click(function(e){
        openbox('box', this);
        return false;
    });
    $("#toggle_chat").click(function(){
        if($("#toggle_chat").prop("checked")) {
            $('.chat').show();
        }else {
            $('.chat').hide();
        }
    });


    /* deletes checked attribute, when page is refreshed */
//    var allCheckboxes = $(".messages_container input:checkbox:enabled");
//    allCheckboxes.removeAttr('checked');
    $('#toggle_chat').trigger('click');
    $('#toggle_chat').prop('checked');

    function openbox(id, toggler) {
        var div = document.getElementById(id);
        if(div.style.display == 'block') {
            div.style.display = 'none';
            toggler.innerHTML = 'Setting';
        } else {
            div.style.display = 'block';
            toggler.innerHTML = 'Close';
        }
    }

    });
    jQuery(document).ready(function(){
        jQuery('.window_chat').scrollbar();
    });

    return {
        ChessChat : ChessChat,
    };

});

