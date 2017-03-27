$(document).ready(function() {

    var storage_create_game = localStorage;
    var CreateGame = openerp.CreateGame = {};
    CreateGame.GameStatusManager = openerp.Widget.extend({
        init: function(model_game_id, dbname, uid){
            this._super();
            var self = this;
            this.game_id = model_game_id;
            openerp.session = new openerp.Session();
            this.start();
            this.c_manager = new openerp.ChessGame.GameManager(model_game_id, dbname, uid).then(function(){
            self.start();});
        },
        start: function(){
            var self = this;
            openerp.session.rpc("/chess/game/status/", {game_id: self.game_id})
                .then(function(result) {
                    if(result=="Active game") {
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
        window.create_new_game = new CreateGame.GameStatusManager(window.model_game_id, window.model_dbname, window.model_author_id);
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
