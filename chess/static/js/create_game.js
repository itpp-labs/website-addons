odoo.define('chess.create_game', function (require) {
"use strict";
var Widget = require('web.Widget');
var session = require('web.session');
var storage_create_game = localStorage;
var CreateGame = {};
var bus = require('bus.bus');
var ChessGame = require('chess.common').ChessGame;

CreateGame.GameStatusManager = Widget.extend({
    init: function(model_game_id, dbname, uid){
        this._super();
        this.game_id = model_game_id;
        this.start();
        this.c_manager = new ChessGame.GameManager(model_game_id, dbname, uid);

    },
    start: function(){
        var self = this;
        session.rpc("/chess/game/status/", {game_id: self.game_id})
            .then(function(result) {
                if(result=="Active game") {
                    window.new_game = new ChessGame.GameConversation(window.model_game_id, window.model_dbname, window.model_author_id);
                    window.new_game.game_pgn_click();
                }
                if(result=="Waiting") {
                    swal("Wait for invitation acceptance", "Your opponent can do it via Chess menu at the backend");
                }
                if(result=="Game Over") {
                    swal({title:'Finished',
                          text:'This game is already finished.',
                          type: 'error'
                          },
                    function(isConfirm) {
                        if (window.tournament) {
                            window.location.replace('/chess/tournament/' + window.tournament);
                        } else {
                        window.location.replace('/chess/');
                    }
                    }
                    );
                return false;
                }
            });
    }
});
$(document).ready(function() {
    if (window.model_game_id === undefined) {
        return false;
    } else {
        window.create_new_game = new CreateGame.GameStatusManager(window.model_game_id, window.model_dbname, window.model_author_id);

    }

    if (window.new_game === undefined) {
        return false;
    }

});

});

$(document).ready(function() {
$('#create_game #blitz, #play_with_a_friend #blitz, #create_tournament #blitz').click(function () {
    $('#create_game #time').show();
    $('#play_with_a_friend #time').show();
    $('#create_tournament #time').show();
});
$('#create_game .limited_time, #play_with_a_friend .limited_time, #create_tournament .limited_time').click(function () {
    $('#create_game #time').show();
    $('#play_with_a_friend #time').show();
    $('#create_tournament #time').show();
});
$('#create_game #standart, #play_with_a_friend #standart, #create_tournament #standart').click(function () {
    $('#create_game #time').hide();
    $('#play_with_a_friend #time').hide();
    $('#create_tournament #time').hide();
});

});
