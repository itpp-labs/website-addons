$(document).ready(function() {

    var storage_create_game = localStorage;
    var CreateGame = openerp.CreateGame = {};
    CreateGame.GameManager = openerp.Widget.extend({
        init: function(model_game_id, dbname, uid) {
            this._super();
            var self = this;
            //add channel for information by game
            var channel_game_info = JSON.stringify([dbname, 'chess.game.info', [uid, model_game_id]]);
            var bus_last = 0;
            Number(storage_create_game.getItem("bus_last"))==null ? bus_last=this.bus.last : bus_last=Number(storage_create_game.getItem("bus_last"));
            // start the polling
            this.bus = openerp.bus.bus;
            this.bus.last = bus_last;
            this.bus.add_channel(channel_game_info);
            this.bus.on("notification", this, this.on_notification);
            this.bus.start_polling();
        },
        on_notification: function (notification) {
            var self = this;
            if (typeof notification[0][0] === 'string') {
                notification = [notification];
            }
            for (var i = 0; i < notification.length; i++) {
                var channel = notification[i][0];
                var message = notification[i][1];
                this.on_notification_do(channel, message);
            }
        },
        on_notification_do: function (channel, message) {
            var self = this;
            var channel = JSON.parse(channel);
            var error = false;
            if (Array.isArray(channel) && channel[1] === 'chess.game.info') {
                try {
                    this.create_game(message);
                } catch (err) {
                    error = err;
                    console.error(err);
                }
            }
        },
        create_game: function(message){
            if(message.system_status=="Active game") {
                create_new_game.stop_polling();
                window.new_game = new openerp.ChessGame.GameConversation(window.model_game_id, window.model_dbname, window.model_author_id);
                window.new_game.game_pgn_click();
                swal({   title: "Lets go!",   timer: 1000,   showConfirmButton: false });
                storage_create_game.setItem("bus_last", this.bus.last);
            }
            if(message.system_status=="Canceled") {
                create_new_game.stop_polling();
                swal("Game canceled");
                return false;
            }
            if(message.system_status=="Denied") {
                create_new_game.stop_polling();
                swal("User refused to play");
                return false;
            }
        }
    });

    CreateGame.GameStatusManager = openerp.Widget.extend({
        init: function(model_game_id, dbname, uid){
            this._super();
            var self = this;
            this.game_id = model_game_id;
            openerp.session = new openerp.Session();
            this.c_manager = new openerp.CreateGame.GameManager(model_game_id, dbname, uid);
            this.start();
        },
        start: function(){
            var self = this;
            openerp.session.rpc("/chess/game/status/", {game_id: self.game_id})
                .then(function(result) {
                    if(result=="Active game") {
                        self.stop_polling();
                        window.new_game = new openerp.ChessGame.GameConversation(window.model_game_id, window.model_dbname, window.model_author_id);
                        window.new_game.game_pgn_click();
                    }
                    if(result=="Canceled") {
                        self.stop_polling();
                        swal("Game canceled");
                        return false;
                    }
                    if(result=="Denied") {
                        self.stop_polling();
                        swal("User refused to play");
                        return false;
                    }
                    if(result=="Waiting") {
                        swal("Wait for invitation acceptance", "Your opponent can do it via Chess menu at the backend");
                    }
                    if(result=="Game Over") {
                        self.stop_polling();
                        window.new_game = new openerp.ChessGame.GameConversation(window.model_game_id, window.model_dbname, window.model_author_id);
                        window.new_game.game_pgn_click();
                        return false;
                    }
                });
        },
        stop_polling: function () {
            openerp.bus.bus.stop_polling();
        }
    });

    if (window.model_game_id===undefined) {
        return false;
    } else {
        var create_new_game = new CreateGame.GameStatusManager(window.model_game_id, window.model_dbname, window.model_author_id);
    }

    if (window.new_game===undefined) {
        return false;
    }
});
$('#create_game #blitz, #play_with_a_friend #blitz').click(function () {
    $('#create_game #time').show();
    $('#play_with_a_friend #time').show();
});
$('#create_game .limited_time, #play_with_a_friend .limited_time').click(function () {
    $('#create_game #time').show();
    $('#play_with_a_friend #time').show();
});
$('#create_game #standart, #play_with_a_friend #standart').click(function () {
    $('#create_game #time').hide();
    $('#play_with_a_friend #time').hide();
});