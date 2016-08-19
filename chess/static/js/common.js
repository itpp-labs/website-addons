$(document).ready(function() {
    "use strict";
    var pos = [];
    var game = {};
    var board ={};
    var turn = '';
    var storage = localStorage;
    var ChessGame = openerp.ChessGame = {};
    var first_step_move = true;
    var author_player_color = '';
    var another_player_color = '';
    var not_win_user_id = '';
    var time_limited = false;
    var start_time_refer = true;
    var ref_bw = true;
    ChessGame.COOKIE_NAME = 'chessgame_session';
    ChessGame.GameManager = openerp.Widget.extend({
        init: function (model_game_id, dbname, uid) {
            this._super();
            var self = this;
            this.game_id = model_game_id;
            var channel_line = JSON.stringify([dbname, 'chess.game.line', [uid, this.game_id]]);
            var channel_game = JSON.stringify([dbname, 'chess.game', [uid, this.game_id]]);
            var bus_last = 0;
            Number(storage.getItem("bus_last"))==null ? bus_last=this.bus.last : bus_last=Number(storage.getItem("bus_last"));

            // start the polling
            this.bus = openerp.bus.bus;
            this.bus.last = bus_last;
            this.bus.add_channel(channel_line);
            this.bus.add_channel(channel_game);
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
            if (Array.isArray(channel) && (channel[1] === 'chess.game.line' || channel[1] === 'chess.game')) {
                try {
                    this.received_message(message);
                } catch (err) {
                    error = err;
                    console.error(err);
                }
            }
        },
        received_message: function(message) {
            var self = this;
            var error = false;
            try {
                if(!message) {
                    return false;
                }
                if (message.type == 'move') {
                    self.onDrop(message.data.source, message.data.target);
                    board.position(game.fen());
                    if(new_game.game_type=='blitz') {
                        if(game.turn()=== 'b') {
                            new_game.clockClicked(1);
                            new_game.clockClicked(0);
                        }
                        if(game.turn()=== 'w') {
                            new_game.clockClicked(0);
                            new_game.clockClicked(1);
                        }
                    }
                    if(new_game.game_type=='limited time' && ref_bw) {
                        if(game.turn()=== 'b') {
                            new_game.clockClicked(1);
                            new_game.clockClicked(0);
                        }
                        if(game.turn()=== 'w') {
                            new_game.clockClicked(0);
                            new_game.clockClicked(1);
                        }
                        ref_bw = false;
                    }
                    storage.setItem("bus_last", this.bus.last);
                }
                if (message.type == 'system'){
                    if (message.data.status == 'surrender') {
                        swal({
                            title: "You win!",
                            text: message.data.user + ' surrendered',
                            timer: 2000,
                            type: "success",
                            showConfirmButton: false
                        });
                        $('#surrender').hide();
                        $('#suggest_a_draw').hide();
                        var status = 'You win, ' + message.data.user + ' surrendered';
                        new_game.user_surrender(status);
                    }
                    if (message.data.status == 'draw') {
                        swal({
                            title: "Draw",
                            text: "The "+ message.data.user+" proposed a draw",
                            type: "warning",
                            showCancelButton: true,
                            confirmButtonColor: "#DD6B55",
                            confirmButtonText: "Yes",
                            cancelButtonText: "No",
                            closeOnConfirm: false
                        },
                            function(isConfirm){
                                if (isConfirm) {
                                    swal({
                                        title: "Game over",
                                        text: "Drawn position",
                                        timer: 2000,
                                        type: "success",
                                        showConfirmButton: false
                                    });
                                    $('#surrender').hide();
                                    $('#suggest_a_draw').hide();
                                    var data = {'status': 'agreement'};
                                    var message = {'type': 'system', 'data': data};
                                    new_game.send_move(message);
                                    new_game.game_over("Game over, draw position");
                                }
                            });
                    }
                    if (message.data.status == 'agreement') {
                        swal({
                            title: "Game over",
                            text: "Drawn position",
                            timer: 2000,
                            type: "success",
                            showConfirmButton: false
                        });
                        $('#surrender').hide();
                        $('#suggest_a_draw').hide();
                        var status = 'Game over, draw position';
                        //delete cookie
                        var cookie_name = ChessGame.COOKIE_NAME+self.game_id;
                        document.cookie = cookie_name + "=" + "; expires=-1";
                        new_game.user_surrender(status);
                    }
                    if (message.data.status == '') {
                        return false;
                    }
                    storage.setItem("bus_last", this.bus.last);
                }
            } catch (err) {
                error = err;
                console.error(err);
            }
        },

        onDrop: function (source, target) {
            var self = this;
            var move = game.move({
                from: source,
                to: target,
                promotion: 'q'
            });
            new_game.onDelFigure();
            new_game.updateStatus();
        }
    });
    ChessGame.GameConversation = openerp.Widget.extend({
        init: function(model_game_id, dbname, uid){
            this._super();
            var self = this;
            openerp.session = new openerp.Session();
            this.c_manager = new openerp.ChessGame.GameManager(model_game_id, dbname, uid);
            console.log("Initial Game");
            this.history = true;
            this.history_loading = false;
            this.surrender_status = false;
            this.coockie_status = false;
            this.check_status = false;
            this.game_over_status = '';
            this.system_status = '';
            this.game_id = model_game_id;

            game = new Chess();
            this.statusEl = $('#status');
            this.fenEl = $('#fen');
            this.pgnEl = $('#pgn');
            this.DelWEl = $('#figure_white');
            this.DelBEl = $('#figure_black');
            /*some figures were removed*/
            this.OLD_FEN_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR';
            this.lenOldFen = ((this.OLD_FEN_POSITION.split('/')).join('')).replace(/[0-9]/g, '').length;
            this.start();
        },
        start: function(){
            var self = this;
            var cookie_name = ChessGame.COOKIE_NAME+self.game_id;
            //when game to finished is coockies is delete
            var cookie = openerp.get_cookie(cookie_name);
            var ready;
            if (!cookie) {
                openerp.session.rpc("/chess/game/init", {game_id: self.game_id})
                    .then(function(result) {
                        //author
                        self.author_name = result.author.name;
                        self.author_id = result.author.id;
                        self.author_color = result.author.color;
                        self.author_time = result.author.time;

                        turn = self.author_color;
                        //another user
                        self.another_user_name = result.another_user.name;
                        self.another_user_id = result.another_user.id;
                        self.another_user_color = result.another_user.color;
                        self.another_user_time = result.another_user.time;

                        //game information
                        self.game_id = result.information.id;
                        self.game_type = result.information.type;
                        self.onGameType(self.game_type, self.author_time, self.another_user_time);
                        self.game_status = result.information.status;
                        self.system_status = result.information.system_status;
                        self.orientation = self.onOrientation();
                        if(self.system_status=='Game Over'){
                            $('.chess_information .chess_time_usr').hide();
                            self.clockStop();
                        }
                        author_player_color = self.author_id;
                        another_player_color = self.another_user_id;

                        //save all data in coockie
                        openerp.set_cookie(cookie_name, JSON.stringify({
                            'author': {
                                'name': self.author_name,
                                'id':self.author_id,
                                'color':self.author_color,
                                'time':self.author_time
                            },
                            'information': {
                                'id': self.game_id,
                                'type': self.game_type,
                                'status': self.game_status,
                                'system_status': self.system_status
                            },
                            'another_user': {
                                'name': self.another_user_name,
                                'id': self.another_user_id,
                                'color': self.another_user_color,
                                'time': self.another_user_time
                            }
                        }), 90*24*60*60);
                        self.onBoard();
                        self.call_load_system_message(result.information.id);
                    });
            } else {
                var coockie_game = JSON.parse(cookie);
                //author
                self.author_name = coockie_game.author.name;
                self.author_id = coockie_game.author.id;
                self.author_color = coockie_game.author.color;
                turn = self.author_color;

                //another user
                self.another_user_name = coockie_game.another_user.name;
                self.another_user_id = coockie_game.another_user.id;
                self.another_user_color = coockie_game.another_user.color;
                //self.another_user_time = coockie_game.another_user.time;

                //game information
                self.game_id = coockie_game.information.id;
                self.game_type = coockie_game.information.type;
                self.game_status = coockie_game.information.status;
                self.system_status = coockie_game.information.system_status;
                author_player_color = self.author_id;
                another_player_color = self.another_user_id;
                if(self.system_status=='Game Over'){
                    $('.chess_information .chess_time_usr').hide();
                    self.clockStop();
                }
                self.orientation = self.onOrientation();
                self.onBoard();
                self.call_load_system_message(coockie_game.information.id);
            }
        },
        onOrientation: function(){
            if (this.author_color==='black') return 'black';
            else return 'white';
        },
        onBoard: function(){
            this.cfg = {
                moveSpeed: 'slow',
                snapbackSpeed: 500,
                snapSpeed: 100,
                draggable: true,
                position: 'start',
                orientation: this.orientation,
                onDragStart: this.onDragStart,
                onDrop: this.onDrop,
                onSnapEnd: this.onSnapEnd
            };
            board = ChessBoard('board', this.cfg);
            $('#flipOrientationBtn').on('click', board.flip);
            this.updateStatus();
        },
        onGameType: function(game_type, author_time, another_user_time){
            var self = this;
            if(self.system_status=='Game Over'){
                $('.chess_information .chess_time_usr').hide();
            }
            else {
                if (game_type == 'blitz') {
                    $('.chess_information .chess_time_usr').show();
                    if (game.turn() === 'b') {
                        self.reset(Math.round(another_user_time), Math.round(author_time));
                    }
                    if (game.turn() === 'w') {
                        self.reset(Math.round(author_time), Math.round(another_user_time));
                    }
                } else {
                    if (game_type == 'limited time') {
                        $('.chess_information .chess_time_usr').show();
                        if (game.turn() === 'b') {
                            self.reset(Math.round(another_user_time), Math.round(author_time));
                        }
                        if (game.turn() === 'w') {
                            self.reset(Math.round(author_time), Math.round(another_user_time));
                        }

                    } else {
                        $('.chess_information .chess_time_usr').hide();
                    }
                }
            }
        },
        call_load_system_message: function(game_id) {
            var self = this;
            openerp.session.rpc("/chess/game/system_history", {'game_id': game_id }).then(function (result) {
                self.call_load_history(game_id, result);
            });
        },
        call_load_history: function(game_id, result){
            var self = this;
            openerp.session.rpc("/chess/game/history", {'game_id': game_id }).then(function (history) {
                if(history){
                    self.history_loading = true;
                    self.check_status = true;
                    self.coockie_status = true;
                    history.forEach(function (item, i, history) {
                        self.onDrop(item.source, item.target);
                        self.onSnapEnd();
                        first_step_move = false;
                    });
                    if(self.system_status=='Game Over'){
                        $('.chess_information .chess_time_usr').hide();
                        self.load_time_history(history, result);

                    }else {
                        self.load_time_history(history, result);
                    }
                }
                else{
                    var cookie_name = ChessGame.COOKIE_NAME+self.game_id;
                    var cookie = openerp.get_cookie(cookie_name);
                    var coockie_game = JSON.parse(cookie);
                    self.author_time = coockie_game.author.time;
                    self.another_user_time = coockie_game.another_user.time;
                    self.onGameType(self.game_type, self.author_time, self.another_user_time);
                }
            });
        },
        load_time_history: function (history, resultat) {
            var self = this;
            var error = false;
            if (this.history) {
                var time_turn = '';
                if (game.turn() === 'w' && turn === 'white') {
                    time_turn = 'ww';
                }
                if (game.turn() === 'w' && turn === 'black') {
                    time_turn = 'wb';
                }
                if (game.turn() === 'b' && turn === 'white') {
                    time_turn = 'bw';
                }
                if (game.turn() === 'b' && turn === 'black') {
                    time_turn = 'bb';
                }
                if (self.game_type == 'blitz' || self.game_type == 'limited time') {
                    openerp.session.rpc("/chess/game/load_time", {'game_id': self.game_id, 'turn': time_turn})
                        .then(function (result) {
                            self.author_time = result.author_time;
                            self.another_user_time = result.another_user_time;
                            if (self.system_status=='Game Over') {
                                if (self.author_time == 0 || self.another_user_time == 0) {
                                    var status = '';
                                    if ((game.turn() === 'w' && turn === 'white') || (game.turn() === 'b' && turn === 'black')) {
                                        status = 'Game over, time limit. You lose';
                                    }
                                    if ((game.turn() === 'w' && turn === 'black') || (game.turn() === 'b' && turn === 'white')) {
                                        status = 'Game over, time limit. You win!';
                                    }
                                    self.user_surrender(status);
                                }else {
                                    self.onGameType(self.game_type, self.author_time, self.another_user_time);
                                    self.showConfirmation(history, resultat);
                                }
                            } else {
                                if (self.author_time == 0 || self.another_user_time == 0) {
                                    self.onGameType(self.game_type, self.author_time, self.another_user_time);
                                    var status = '';
                                    if ((game.turn() === 'w' && turn === 'white') || (game.turn() === 'b' && turn === 'black')) {
                                        status = 'Game over, time limit. You lose';
                                        self.game_over_status = self.author_color;
                                    }
                                    if ((game.turn() === 'w' && turn === 'black') || (game.turn() === 'b' && turn === 'white')) {
                                        status = 'Game over, time limit. You win!';
                                        self.game_over_status = self.another_user_color;
                                    }
                                    self.game_over(status);
                                } else {
                                    self.onGameType(self.game_type, self.author_time, self.another_user_time);
                                    self.showConfirmation(history, resultat);
                                }
                            }
                        });
                }
                else {
                    self.showConfirmation(history, resultat);
                }
            }
        },
        showConfirmation: function(history, result){
            var self = this;
            if (this.history){
                if(self.game_type=='blitz') {
                    if(game.turn()=== 'b') {
                        self.clockClicked(1);
                    }
                    if(game.turn()=== 'w') {
                        self.clockClicked(0);
                    }
                }

                if (self.game_type=='limited time' && start_time_refer) {
                    if(game.turn()=== 'b') {
                        self.clockClicked(1);
                    }
                    if(game.turn()=== 'w') {
                        self.clockClicked(0);
                    }
                }
                start_time_refer = false;
                self.onSnapEnd();
                if (result.type == 'system') {
                    switch (result.data.status) {
                        case 'surrender': {
                            if (result.data.user==self.author_name) {
                                var status = 'Game over, you lose. You surrender';
                                self.user_surrender(status);
                                self.game_over_status = self.author_color;
                            }
                            else {
                                var status = 'Game over, you win! '+self.another_user_name + ' is surrender';
                                self.game_over_status = self.another_user_color;
                                self.user_surrender(status);
                            }
                        } break;
                        case 'draw': {
                            if (result.data.user!=self.author_name) {
                                setTimeout(function () {
                                swal({
                                    title: "Draw",
                                    text: "The "+ self.another_user_name + " proposed a draw",
                                    type: "warning",
                                    showCancelButton: true,
                                    confirmButtonColor: "#DD6B55",
                                    confirmButtonText: "Yes",
                                    cancelButtonText: "No",
                                    closeOnConfirm: false
                                },
                                    function(isConfirm){
                                        if (isConfirm) {
                                            swal({
                                                title: "Game over",
                                                text: "Drawn position",
                                                timer: 2000,
                                                type: "success",
                                                showConfirmButton: false
                                            });
                                            var data = {'status': 'agreement', 'user': self.author_name};
                                            var message = {'type': 'system', 'data': data};
                                            var status = 'Game over, drawn position';
                                            self.send_move(message);
                                            self.user_surrender(status);
                                        }
                                    });},1000);
                            }

                        } break;
                        case 'agreement':{
                            var status = 'Game over, drawn position';
                            self.game_over_status='drawn';
                            self.user_surrender(status);
                        } break;
                        case 'Game over': {
                            var status = 'Game over';
                            self.user_surrender(status);
                        } break;
                        default:{
                            console.log("No match in the system messages");
                        } break;
                    }
                }
                else {console.log("No system messages");}
            }
            this.history=false;
        },
        onDragStart: function (source, piece, position, orientation) {
            var self = this;
            board.position(game.fen());
            var game_queue=false;
            if(game.turn() === 'w' && turn == 'white')
            {
                game_queue=true;
            }
            if(game.turn() === 'b' && turn == 'black')
            {
                game_queue=true;
            }
            if(game_queue==true) {
                if (game.game_over() === true ||
                    (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
                    (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
                    return false;
                }
            }
            else{
                return false;
            }
        },
        onDrop: function (source, target) {
            var self = this;
            // see if the move is legal
            var move = game.move({
                from: source,
                to: target,
                promotion: 'q' // NOTE: always promote to a queen for example simplicity
            });
            // illegal move
            if (move === null) return 'snapback';
            else {
                if (self.history_loading != true) {
                    var data = {'source': source, 'target': target, 'fen': game.fen()};
                    var message = {'type': 'move', 'data': data};
                    new_game.send_move(message);
                }
            }
            new_game.onDelFigure();
            new_game.updateStatus();
        },
        send_move: function(message){
            var self = this;
            self.check_status = false;
            self.coockie_status = true;
            ref_bw = true;
            openerp.session.rpc("/chess/game/send/", {message: message, game_id: self.game_id})
                .then(function(result){
                    if(result=='move'){
                        if(self.game_type=='blitz') {
                            if (game.turn() === 'w') {
                                var data = {'status': 'time', 'user': self.author_name, 'value': self.times[1]};
                                var message = {'type': 'system', 'data': data};
                                self.send_move(message);
                                self.clockClicked(1);
                            }
                            if (game.turn() === 'b') {
                                var data = {
                                    'status': 'time',
                                    'user': self.author_name,
                                    'value': self.times[0]
                                };
                                var message = {'type': 'system', 'data': data};
                                self.send_move(message);
                                if (first_step_move) {
                                    self.clockClicked(1);
                                } else {
                                    self.clockClicked(0);
                                }
                            }
                        }
                        if(self.game_type=='limited time') {
                            if (game.turn() === 'w') {
                                self.reset(Math.round(self.another_user_time), Math.round(self.author_time));
                                self.clockClicked(0);

                            }
                            if (game.turn() === 'b') {
                                self.reset(Math.round(self.author_time), Math.round(self.another_user_time));
                                self.clockClicked(1);

                            }
                        }
                        first_step_move = false;
                    }
                    else if (result=='system') {
                        //console.log("Send system message");
                    }
                    else {
                        console.log("ERROR, please make the right move");
                        return self.user_surrender('ERROR, please make the right move');
                    }
                });
        },
        onSnapEnd: function () {
            // update the board position after the piece snap
            // for castling, en passant, pawn promotion
            board.position(game.fen());
        },
        updateStatus: function () {
            var self = this;
            var status = '';
            var moveColor = 'White';
            if (game.turn() === 'b') {
                moveColor = 'Black';
            }
            var typea = "success",
                check = "";
            if (moveColor == "White") {
                typea = "warning";
            }
            // checkmate?
            if (game.in_checkmate() === true) {
                if((game.turn()=== 'b' && self.author_color=='black') || (game.turn() === 'w' && self.author_color=='white')) {
                    setTimeout(function () {swal("Game Over", moveColor + " is in checkmate. You lose", "error");}, 100);
                    status = moveColor + ' is in checkmate. You lose';
                }
                if((game.turn()=== 'b' && self.author_color=='white') || (game.turn()=== 'w' && self.author_color=='black')) {
                    setTimeout(function () {swal("Game Over", moveColor + " is in checkmate. You win!", "success");}, 100);
                    status = moveColor + ' is in checkmate. You win!';
                }
                self.game_over_status = moveColor;
                $('.chess_information .chess_time_usr').hide();
                if (self.game_status!='Game Over') {
                    self.game_over(moveColor + " is in checkmate.");
                }
                self.user_surrender(status);
            }
            // draw?
            else if (game.in_draw() === true) {
                status = 'Game over, drawn position.';
                setTimeout(function () {swal("Game Over", "is drawn position", "error");}, 100);
                self.game_over_status='drawn';
                if (self.game_status!='Game Over') {
                    self.game_over("Game Over, is drawn position");
                }
            }
            // game still on
            else {
                status = moveColor + ' to move';
                // check?
                if (game.in_check() === true) {
                    if (self.check_status == false) {
                        status += ', ' + moveColor + ' is in check';
                        setTimeout(function () {
                            swal({
                                title: moveColor + ' is in check',
                                text: moveColor + ' to move',
                                timer: 1000,
                                showConfirmButton: false
                            });
                            var data = {'status': 'check', 'user': self.author_name};
                            var message = {'type': 'system', 'data': data};
                            self.send_move(message);

                        }, 100);
                    }
                    status = moveColor + ' is in check';
                }
            }
            //surrender?
            if (this.surrender_status==false){
                $('.end_game #surrender').click(function () {
                    this.surrender_status=true;
                    setTimeout(function () {
                        swal({
                                title: "Are you sure?",
                                text: "You will lose",
                                type: "warning",
                                showCancelButton: true,
                                confirmButtonColor: "#DD6B55",
                                confirmButtonText: "Yes",
                                cancelButtonText: "No",
                                closeOnConfirm: false
                            },
                            function (isConfirm) {
                                if (isConfirm) {
                                    swal({
                                        title: "Game over",
                                        text: 'You lose',
                                        timer: 2000,
                                        type: "error",
                                        showConfirmButton: false
                                    });
                                    status = 'Game over, you lose. You surrender';
                                    //send system message (user is surrender)
                                    if (self.coockie_status) {
                                        var data = {'status': 'surrender', 'user': self.author_name};
                                        var message = {'type': 'system', 'data': data};
                                        self.send_move(message);
                                        self.game_over_status=self.author_color;
                                        self.game_over(status);
                                    }
                                }
                            });
                    }, 100);
                });

            } else {
                status = 'Game over, you lose';
                self.game_over_status=self.author_color;
                self.game_over(status);
            }

            // suggest a draw?
            $('.end_game #suggest_a_draw').click(function(){
                swal({
                    title: "Are you sure?",
                    text: "Send a message to offer a draw",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Yes",
                    cancelButtonText: "No",
                    closeOnConfirm: false
                },
                    function(isConfirm){
                        if (isConfirm) {
                            swal({
                                title: 'Message sent',
                                text: 'Wait for an answer from another user',
                                timer: 2000,
                                showConfirmButton: false
                            });
                            $('#suggest_a_draw').hide();

                            //send system message (offer a draw)
                            var data = {'status': 'draw', 'user': self.author_name};
                            var message = {'type': 'system', 'data': data};
                            self.send_move(message);
                        }
                    });
            });
            pos.push(game.fen());
            this.statusEl.html(status);
            this.fenEl.html(game.fen());
            var load_pgn = game.pgn();
            this.pgnEl.html(load_pgn.replace(game.fen(), ''));
        },
        game_over: function(status) {
            if (this.system_status=='Game Over') {
                return false;
            }
            $('.chess_information .chess_time_usr').hide();
            console.log('Game Over');

            //delete cookie
            var cookie_name = ChessGame.COOKIE_NAME+this.game_id;
            document.cookie = cookie_name + "=" + "; expires=-1";

            var self = this;
            var status_game = self.game_over_status;

            if (time_limited) {
                not_win_user_id = not_win_user_id;
            } else {
                not_win_user_id = false;
            }
            openerp.session.rpc("/chess/game/game_over/", {'game_id': self.game_id, 'status': status_game.toLowerCase(), 'time_limit_id': not_win_user_id})
                .then(function(result){
                    if(result) {
                        $('#surrender').hide();
                        $('#suggest_a_draw').hide();
                        self.user_surrender(status);
                    }
                });
        },
        onDelFigure: function () {
            /* It is only important as a shortened post we will use
             only to determine the remote pieces on the board */
            this.NewFenPosition = (game.fen()).split(' ');
            this.OldFenPosition = ((this.OLD_FEN_POSITION.split('/')).join('')).replace(/[0-9]/g, '');
            this.NewFenPosition = ((this.NewFenPosition[0].split('/')).join('')).replace(/[0-9]/g, '');
            var oldArr = (this.OldFenPosition.split('')).sort(),
                newArr = (this.NewFenPosition.split('')).sort();
            this.OldFenPosition = oldArr.join('');
            this.NewFenPosition = newArr.join('');
            /*if not the same as the length of the old with the new, then removed figure*/
            if (this.lenOldFen != this.NewFenPosition.length) {

                var WhiteArr = [], BlackArr = [];
                var pattern = /[A-Z]/;
                for (var i = 0; i < oldArr.length; i++) {
                    var elem = oldArr[i];
                    var index = newArr.indexOf(elem);
                    if (index != -1) {
                        newArr.splice(index, 1);
                    }
                    else {
                        if (pattern.test(elem)) WhiteArr.push(elem);
                        else BlackArr.push(elem);
                    }
                }

                if (WhiteArr.length > 0) {
                    var imagesHTML = {
                        P: "<img src='/chess/static/img/chesspieces/wikipedia/wP.png' alt='white pawn'>",
                        B: "<img src='/chess/static/img/chesspieces/wikipedia/wB.png' alt='white bishop'>",
                        N: "<img src='/chess/static/img/chesspieces/wikipedia/wN.png' alt='white kNight'>",
                        R: "<img src='/chess/static/img/chesspieces/wikipedia/wR.png' alt='white rook'>",
                        Q: "<img src='/chess/static/img/chesspieces/wikipedia/wQ.png' alt='white queen'>"
                    };

                    var data = WhiteArr.reduce(function (result, imageKey) {
                        if (!result[imageKey]) {
                            result[imageKey] = {html: imagesHTML[imageKey], count: 1};
                        } else {
                            result[imageKey].count++;
                        }
                        return result;
                    }, {});

                    var html = '';

                    Object.keys(data).forEach(function (key) {
                        html += data[key].html;
                        if (data[key].count > 1) {
                            html += 'X' + data[key].count;
                        }
                        html += '\n';
                    });
                    var DelWF = html;
                    this.DelWEl.html(DelWF);
                }
                

                if (BlackArr.length > 0) {
                    var imagesHTML = {
                        p: "<img src='/chess/static/img/chesspieces/wikipedia/bP.png' alt='black pawn'>",
                        b: "<img src='/chess/static/img/chesspieces/wikipedia/bB.png' alt='black bishop'>",
                        n: "<img src='/chess/static/img/chesspieces/wikipedia/bN.png' alt='black kNight'>",
                        r: "<img src='/chess/static/img/chesspieces/wikipedia/bR.png' alt='black rook'>",
                        q: "<img src='/chess/static/img/chesspieces/wikipedia/bQ.png' alt='black queen'>"
                    };

                    var data = BlackArr.reduce(function (result, imageKey) {
                        if (!result[imageKey]) {
                            result[imageKey] = {html: imagesHTML[imageKey], count: 1};
                        } else {
                            result[imageKey].count++;
                        }
                        return result;
                    }, {});

                    var html = '';

                    Object.keys(data).forEach(function (key) {
                        html += data[key].html;
                        if (data[key].count > 1) {
                            html += 'X' + data[key].count;
                        }
                        html += '\n';
                    });
                    var DelBF = html;
                    this.DelBEl.html(DelBF);
                }

                this.lenOldFen = this.lenOldFen - 1;
            }
        },
        user_surrender: function (status) {
            var self = this;
            $('.chess_information .chess_time_usr').hide();
            this.statusEl.html(status);
            this.cfg = {
                moveSpeed: 'slow',
                snapbackSpeed: 500,
                snapSpeed: 100,
                orientation: this.orientation,
                position: game.fen(),
            };
            $('#surrender').hide();
            $('#suggest_a_draw').hide();
            board = ChessBoard('board', this.cfg);
            $('#flipOrientationBtn').on('click', board.flip);
            self.clockStop();
            console.log("Game over");
        },
        status : "stopped",
        currentClock : 0,
        times : [ 0, 0 ],
        clockStop: function() {
            var self = this;
            this.clearInterval();
            this.removeClass(this.currentClock, 'expired');
            if ((game.turn() === 'b' && turn=='black') ||  (game.turn() === 'w' && turn=='black')) {
                    self.reset(Math.round(self.another_user_time), Math.round(self.author_time));
            }
            if ((game.turn() === 'w' && turn=='white') || (game.turn() === 'b' && turn=='white')) {
                self.reset(Math.round(self.author_time), Math.round(self.another_user_time));
            }
        },
        clockClicked : function(id) {
            if (game.game_over()==false) {
                var self = this;
                if (this.status == "stopped") {
                    /* start the clock */
                    this.status = "running";
                    this.currentClock = id;
                    this.setInterval();
                    this.addClass(this.currentClock, "running");
                } else if (this.status == "running") {
                    /* clock is already running */
                    if (this.currentClock == id) {
                        /* change the current clock */
                        this.removeClass(this.currentClock, "running");
                        if (this.currentClock == 0) {
                            this.currentClock = 1;
                        } else {
                            this.currentClock = 0;
                        }
                        this.addClass(this.currentClock, "running");
                    }
                } else {
                    self.status = 'expired';
                    /* status is "expired", do nothing */
                }
            }
        },
        setInterval : function() {
            this.timer = window.setInterval(this.countDown, 1000);
        },

        clearInterval : function() {
            if ( this.timer ) {
                window.clearInterval(this.timer);
                this.timer = null;
            }
        },
        countDown : function() {
            var self = this;
            new_game.times[new_game.currentClock]--;
            new_game.updateClock(
                    new_game.currentClock,
                    new_game.times[new_game.currentClock]);
            /* check if zero has been reached */
            if (new_game.times[new_game.currentClock] == 0) {
                /* stop the interval */
                new_game.clearInterval();
                new_game.status = "expired";
                var status = '';
                if ((game.turn() === 'w' && turn === 'white') || (game.turn() === 'b' && turn === 'black')) {
                    status = 'Game over, time limit. You lose =(';
                    swal({
                        title: "Game over",
                        text: "Time limit. You lose",
                        timer: 2000,
                        type: "error",
                        showConfirmButton: false
                    });
                    not_win_user_id = author_player_color;
                    time_limited = true;
                }
                if ((game.turn() === 'w' && turn === 'black') || (game.turn() === 'b' && turn === 'white')) {
                    swal({
                        title: "Game over",
                        text: "Time limit. You win! =)",
                        timer: 2000,
                        type: "success",
                        showConfirmButton: false
                    });
                    status = 'Game over, time limit. You win!';
                    not_win_user_id = another_player_color;
                    time_limited = true;
                }
                if (self.system_status!='Game Over') {
                    new_game.game_over(status);
                }
            }
        },
        reset : function(author_time, another_user_time) {
            /* reset the times */

            this.times = [ author_time, another_user_time];

            /* stop the clock */
            this.status = "stopped";

            this.clearInterval();

            this.removeClass(0, "running");
            this.removeClass(1, "running");

            /* update the view */
            this.updateView();
        },
        updateView : function() {
            this.updateClock(0, this.times[0]);
            this.updateClock(1, this.times[1]);
        },
        updateClock : function(id, time) {
            var self = this;
            element = document.getElementById("clock"+id);
            var formattedTime = this.formatTime(time);
            element.innerHTML = formattedTime;

            /* change the class if time is up */
            if ( time == 0 ) {
                this.addClass(id, "expired");
                this.clearInterval();
            } else {
                /* remove the class "expired" */
                this.removeClass(id, "expired");
            }
        },
        addClass : function(id, className) {
            element = document.getElementById("clock"+id);
            element.className += " " + className;
        },

        removeClass : function(id, className) {
            element = document.getElementById("clock"+id);
            var exp = new RegExp(className);
            element.className = element.className.replace( exp , '' );
        },
        formatTime : function(time) {
            var minutes = Math.floor(time / 60);
            var seconds = Math.floor(time % 60);
            var hours = Math.floor(minutes / 60);
            minutes = Math.floor(minutes % 60);
            var days = Math.floor(hours / 24);
            hours = Math.floor(hours % 24);

            var result = "";
            if (days != 0) result += days + "d ";
            if (hours < 10) result +="0";
            result += hours + ":";
            if (minutes < 10) result += "0";
            result += minutes + ":";
            if (seconds < 10) result += "0";
            result += seconds;

            return result;
        },
        game_pgn_click: function(){
            new_game.pgnEl.on('click', 'a',function(event) {
                event.preventDefault();
                var data = $(this).data('move').split(',');
                var i = $(this).index();
                board.position(pos[i], false);
                board.move.apply(null, data);
            });
        }
    });

    var element = document.getElementById('board');
    if (!element) {
        return;
    }

    openerp.set_cookie = function(name, value, ttl) {
        ttl = ttl || 24*60*60*365;
        document.cookie = [
            name + '=' + value,
            'path=/',
            'max-age=' + ttl,
            'expires=' + new Date(new Date().getTime() + ttl*1000).toGMTString()
        ].join(';');
    };

});
