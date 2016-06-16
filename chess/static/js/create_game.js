$(document).ready(function() {

    var CreateGame = openerp.CreateGame = {};
    CreateGame.GameManager = openerp.Widget.extend({
        init: function(model_game_id, dbname, uid) {
            this._super();
            var self = this;

            var channel_game_info = JSON.stringify([dbname, 'chess.game.info', [uid, this.game_id]]);

            // start the polling
            this.bus = openerp.bus.bus;
			this.bus.add_channel(channel_game_info);
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
                this.bus.stop_polling();
                console.log("Загрузка информации с лонг поллинга");
                //window.new_game = new openerp.ChessGame.GameConversation(window.model_game_id, window.model_dbname, window.model_author_id);
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
                        openerp.bus.bus.stop_polling();
                        console.log("Загрузка информации с БД");
                        window.new_game = new openerp.ChessGame.GameConversation(window.model_game_id, window.model_dbname, window.model_author_id);
                    }
                })
        }
    });

    if (window.model_game_id===undefined) {
        return false;
    } else {
        var create_new_game = new CreateGame.GameStatusManager(window.model_game_id, window.model_dbname, window.model_author_id);
    }

    if (window.new_game===undefined) {
        return false;
    } else {
        new_game.pgnEl.on('click', 'a',function(event) {
            event.preventDefault();
            var data = $(this).data('move').split(',');
            var i = $(this).index();
            board.position(pos[i],false);
            board.move.apply(null,data);
	    });
        return false;
    }

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
});