odoo.define('chess.tournament', function (require) {
'use strict';
var Widget = require('web.Widget');
var Model = require('web.Model');
var core = require('web.core');
var session = require('web.session');

var QWeb = core.qweb;

var TournamentsController = Widget.extend({
    template: 'TournamentsMain',
    events: {'click .tournament_list_element': 'show_table'},

    start: function() {
        this.list = new TournamentsList();
        this.list.appendTo(this.$el);
    },

    show_table: function(event) {
        var res_id = $(event.currentTarget).data('id');
        this.list.destroy();
        this.detail = new TournamentDetail(res_id);
        this.detail.appendTo(this.$el);
    }
});
core.action_registry.add('tournament_action', TournamentsController);


var TournamentsList = Widget.extend({
    template: 'TournamentsListTemplate',
    start: function() {
        this.show_tournaments_list();
    },

    show_tournaments_list: function() {
        var self = this;
        return new Model('chess.tournament')
            .query(['start_date', 'tournament_type','create_uid'])
            .filter([['status', '=', 'Active']])
            .all().then(
                function(results) {
                    _(results).each(function(item) {
                        self.$el.append(QWeb.render('TournamentListElement', {item: item}));
                    });
                });
    }
});

var TournamentDetail = Widget.extend({
//    template: 'TournamentTableTemplate',
    init: function(res_id) {
        this._super(parent);
        this.res_id = res_id;
    },
    start: function() {
        var self = this;
        var tournament = new Model('chess.tournament')
            .call('send_tournament_players_data', [this.res_id])
            .then(function(tournament_data) {
                self.players = tournament_data.players;
                self.tournament_type = tournament_data.tournament_type;
                self.tournament_time = tournament_data.time_data;
                self.fetch_game_data();
            });
    },

    fetch_game_data: function() {
        var self = this;
        var games = new Model('chess.game')
            .call('send_games_data', [this.res_id])
            .then(function(games_data){
                self.games_data = games_data;
                self.render_table();
            });
    },

    render_table: function() {
            var $table = $('<table/>').addClass('tournament-table');
            this.$el.append($table);
            this.render_header($table);
            for (var i=0;i<this.players.length;i++) {
                var $row = $('<tr/>');
                $table.append($row);
                this.render_row($row, this.players[i]);
            }
    },

    render_header: function($table) {
        var $header = $('<tr/>').addClass('header-row');
        $table.append($header);

        var $emptyTd = $('<td/>').addClass('empty-td');
        $header.append($emptyTd);

        for (var i=0; i<this.players.length;i++) {
            var $header_cell = $('<td/>').addClass('header-cell');
            $header.append($header_cell);
            this.render_title($header_cell, this.players[i]);
        }
        var $score_cell = $('<td/>').addClass('score-cell');
        $score_cell.append('<h3>Final Score</h3>');
        $header.append($score_cell);
    },

    render_row: function($row, player) {
        var $row_title = $('<td/>').addClass('row-title');
        this.render_title($row_title, player);
        $row.append($row_title);
        for (var i=0;i<this.players.length;i++) {
            if(this.same_user_game($row, player, this.players[i])) {
                continue;
            }
            this.render_game_cell($row, player, this.players[i]);

        }
        this.show_score($row, player);
    },

    show_score: function($row, player) {
        var score = 0;
        for (var i=0;i<this.games_data.length;i++){
            if (this.games_data[i].player1.id == player.id) {
                score += Number(this.games_data[i].player1.score);
            } else if (this.games_data[i].player2.id == player.id) {
                score += Number(this.games_data[i].player2.score);
            }
        }
        var $cell = $('<td/>').addClass('players-score');
        $cell.append('<h1>'+score+'<h1/>');
        $row.append($cell);
    },

    render_game_cell: function($row, rowPlayer, columnPlayer) {
        for (var i=0; i<this.games_data.length; i++) {
            if (this.player_in_game(rowPlayer, this.games_data[i]) && this.player_in_game(columnPlayer, this.games_data[i])) {
                this.render_game($row, this.games_data[i], rowPlayer, columnPlayer);
                return;
            }
        }
        if ((session.uid == rowPlayer.id)||(session.uid == columnPlayer.id)) {
            var second_player = (session.uid === rowPlayer.id) ? columnPlayer.id: rowPlayer.id;
            var GameCell = new StartGameCell(this.res_id, second_player, this.tournament_type, this.tournament_time);
            GameCell.appendTo($row);
        } else {
            this.render_has_not_started_game($row);
        }
    },

    render_has_not_started_game: function($row) {
        var $cell = $('<td/>').addClass('has_not_started');
        $cell.append('<p> Game has not started yet. </p>');
        $row.append($cell);
    },

    render_game: function($row, game, rowPlayer, columnPlayer) {
        if (((game.system_status == 'Waiting') || (game.system_status == 'Active game')) &&
        ((session.uid == rowPlayer.id)||(session.uid == columnPlayer.id))) {
            new ToMyGameCell(game).appendTo($row);
            return;
        } else if (game.system_status == 'Game Over') {
            this.render_finished_game($row, game, rowPlayer, columnPlayer);
        } else {
            var $cell = $('<td/>').addClass('in-progress');
            $cell.append('<p> Game in progress. </p>');
            $row.append($cell);
        }

    },

    player_in_game: function(player, game) {
        return ((player.id === game.player1.id)||(player.id === game.player2.id));
    },

    same_user_game: function($row, rowPlayer, columnPlayer) {
        if (rowPlayer == columnPlayer) {
            var $cell = $('<td/>').addClass('empty-cell');
            $row.append($cell);
            return true;
        }
    },

    render_title: function($cell, player) {
        $cell.append('<span>' + player.name +'<span/>');
    },

    render_finished_game: function($row, game, rowPlayer, columnPlayer) {
        var player = (game.player1.id == rowPlayer.id) ? game.player1: game.player2;
        var $cell = $('<td/>').addClass('finished-game');
        $cell.append('<h1>' + player.score + '</h1>');
        $row.append($cell);
    }
});

var StartGameCell = Widget.extend({
    template: 'TournamentTableStartGameCell',
    events: {'click': 'start_game'},
    init: function(tournament_id, opponent, tournament_type, tournament_time) {
        this.tournament_id = tournament_id;
        this.opponent = opponent;
        this.tournament_type = tournament_type;
        this.time_d = tournament_time.time_d,
        this.time_h = tournament_time.time_h,
        this.time_m = tournament_time.time_m,
        this.time_s = tournament_time.time_s,
        this._super(parent);
    },

    start: function() {
        this.$el.addClass('start-game-cell');
        this.$el.append('<h3>Start Game</h3>');
    },

    start_game: function() {
        var self = this;
        new Model('chess.game')
            .call('create_tournament_game', [],
                {
                    tournament_id: self.tournament_id,
                    game_type: self.tournament_type,
                    first_user_id: session.uid,
                    second_user_id: self.opponent,
                    time_d: self.time_d,
                    time_h: self.time_h,
                    time_m: self.time_m,
                    time_s: self.time_s
                }
            ).then(function(result){
                window.location.replace('/chess/game/'+result);
            });
    }
});

var ToMyGameCell = Widget.extend({
    template: 'TournamentTableToMyGameCell',
    events: {'click': 'to_the_game'},
    init: function(game) {
        this.game = game;
        this._super(parent);
    },
    start: function() {
        this.$el.addClass('my-game-in-progress');
        this.$el.append('<h3>Enter the game</h3>');
    },

    to_the_game: function() {
        var self = this;
        if (this.game.system_status == 'Waiting') {
            new Model('chess.game')
                .call('accept_tournament_game', [this.game.id])
                .then(function(result) {
                    window.location.replace('/chess/game/'+self.game.id);
                });
        } else {
        window.location.replace('/chess/game/'+ this.game.id);
        }
    }
});

return { TournamentDetail: TournamentDetail,
         StartGameCell: StartGameCell,
         ToMyGameCell: ToMyGameCell
         };

});

