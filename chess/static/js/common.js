(function() {
	"use strict";
	var pos = [];
	var game = {};
	var board ={};
	var ChessGame = openerp.ChessGame = {};
    ChessGame.COOKIE_NAME = 'chessgame_session';
	ChessGame.GameManager = openerp.Widget.extend({
		init: function (parent) {
            this._super(parent);
            console.log("Initial polling widget for game");
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
            } catch (err) {
                error = err;
                console.error(err);
            }
        }

	});
	ChessGame.GameConversation = openerp.Widget.extend({
		init: function(parent){
			this._super(parent);
			var self = this;
			this.c_manager = new openerp.ChessGame.GameManager(this);
			console.log("Initial chess game");
			this.history = true;
			this.history_loading = false;
			this.surrender_status = false;
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
			this.cfg = {
				moveSpeed: 'slow',
				snapbackSpeed: 500,
				snapSpeed: 100,
				draggable: true,
				position: 'start',
				onDragStart: this.onDragStart,
				onDrop: this.onDrop,
				onSnapEnd: this.onSnapEnd
			};
			board = ChessBoard('board', this.cfg);
			$('#flipOrientationBtn').on('click', board.flip);
			self.updateStatus();
		},
		start: function(){
			var self = this;
			var local_id = (location.href).split('/');
            var len_local_id = local_id.length;
            self.game_id = local_id[len_local_id-2];
            var cookie_name = ChessGame.COOKIE_NAME+self.game_id;
            //when game to finished is coockies is delete
            var cookie = openerp.get_cookie(cookie_name);
            var ready;
			if (!cookie) {
                console.log("Init and create coockie for game");
                openerp.jsonRpc("/chess/game/init", "call", {game_id: self.game_id})
					.then(function(result) {
						//author
						self.author_name = result.author.name;
						self.author_id = result.author.id;
						self.author_color = result.author.color;

						//another user
						self.another_user_name = result.another_user.name;
						self.another_user_id = result.another_user.id;
						self.another_user_color = result.another_user.color;

						//game information
						self.game_id = result.information.id;
						self.game_type = result.information.type;
						self.game_time = result.information.time;
						self.game_status = result.information.status;

						//save all data in coockie
						openerp.set_cookie(cookie_name, JSON.stringify({
							'author': {
								'name': self.author_name,
								'id':self.author_id,
								'color':self.author_color
							},
							'information': {
								'id': self.game_id,
								'type': self.game_type,
								'time': self.game_time,
								'status': self.game_status
							},
							'another_user': {
								'name': self.another_user_name,
								'id': self.another_user_id,
								'color': self.another_user_color
							}
						}), 60*60);
						self.call_load_history(result.information.id);
					});
            } else {
                console.log("Load history and coockie for game");
                var game = JSON.parse(cookie);
				//author
				self.author_name = game.author.name;
				self.author_id = game.author.id;
				self.author_color = game.author.color;

				//another user
				self.another_user_name = game.another_user.name;
				self.another_user_id = game.another_user.id;
				self.another_user_color = game.another_user.color;

				//game information
				self.game_id = game.information.id;
				self.game_type = game.information.type;
				self.game_time = game.information.time;
				self.game_status = game.information.status;
				self.call_load_history(game.information.id);
            }
		},
		call_load_history: function(game_id){
			var self = this;
			openerp.jsonRpc("/chess/game/history", "call", {game_id: self.game_id }).then(function (history) {
				if(history){
					self.history_loading = true;
					self.load_move_history(history);
				}
				else{
					console.log("Not load history. (game)");
				}
			});
		},
		load_move_history: function (history) {
			var self = this;
            var error = false;
			if(this.history) {
                history.forEach(function (item, i, history) {
					self.onDrop(item['source'], item['target']);
                });
				self.onSnapEnd();
            };
            this.history=false;
        },
		onDragStart: function (source, piece, position, orientation) {
			var self = this;
			board.position(game.fen());
			if (game.game_over() === true ||
				(game.turn() === 'w' && piece.search(/^b/) !== -1) ||
				(game.turn() === 'b' && piece.search(/^w/) !== -1)) {
				//(orientation === 'white' && piece.search(/^b/) !== -1) ||
				//(orientation === 'black' && piece.search(/^w/) !== -1)) {
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
					var data = {'source': source, 'target': target};
					var message = {'type': 'move', 'data': data};
					new_game.send_move(message);
					console.log("Source: " + source);
					console.log("Target: " + target);
					console.log("Move: " + source + "-" + target);
					console.log("____________________________");
				}
			}
			new_game.onDelFigure();
			new_game.updateStatus();
		},
		send_move: function(message){
			var self = this;
			console.log("send_move");
			openerp.jsonRpc("/chess/game/send/", 'call', {message: message, game_id: self.game_id})
				.then(function(result){
					if(result){
						console.log("Move is send!!!");
					}
				});
             //   .then(function (result) {
             //       if(result) {
             //           self.received_message(message);
             //       } else {
             //           console.log("error, message is not send");
             //       }
             //   });
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
				status = moveColor + ' is in checkmate.';
				if (self.history_loading != true) {
					swal("Game Over", moveColor + " is in checkmate.", "error");
				}
			}
			// draw?
			else if (game.in_draw() === true) {
				status = 'Game over, drawn position';
				if (self.history_loading != true){
					swal("Game Over", "is drawn position", "error");
				}
			}
			// game still on
			else {
				status = moveColor + ' to move';
				// check?
				if (game.in_check() === true) {
					status += ', ' + moveColor + ' is in check';
					swal({
						title: moveColor + ' is in check',
						text: moveColor + ' to move',
						timer: 1000,
						showConfirmButton: false
					});
				}
			}
			//surrender?
			if (this.surrender_status==false){
				$('.end_game #surrender').click(function () {
					this.surrender_status=true;
					//отправка системного сообщения о том что, пользователь сдался (записывается кто сдался
					//и то, что он сдался
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
						function(isConfirm){
							if (isConfirm) {
								swal({
									title: "Game over",
									text: 'You lose',
									timer: 2000,
									type: "error",
									showConfirmButton: false
								});
								$('#surrender').hide();
								$('#suggest_a_draw').hide();
								status = 'Game over, you lose';
								self.user_surrender(status);
							}
						});
				});

			} else {
				$('#surrender').hide();
				$('#suggest_a_draw').hide();
				status = 'Game over, you lose';
				self.user_surrender(status);
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
						}
					});
			});
			pos.push(game.fen());
			this.statusEl.html(status);
			this.fenEl.html(game.fen());
			var load_pgn = game.pgn()
			this.pgnEl.html(load_pgn.replace(game.fen(), ''));

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
				;

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
			this.statusEl.html(status);
			this. cfg = {
				moveSpeed: 'slow',
				snapbackSpeed: 500,
				snapSpeed: 100,
				position: game.fen(),
			};
			board = ChessBoard('board', this.cfg);
			$('#flipOrientationBtn').on('click', board.flip);
		}
	});

	var element = document.getElementById('board')
	if (!element) {
		return;
	}

	var new_game = new ChessGame.GameConversation();
	new_game.pgnEl.on('click', 'a',function(event) {
		event.preventDefault();
		var data = $(this).data('move').split(',');
		var i = $(this).index();
		board.position(pos[i],false);
		board.move.apply(null,data);
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
})();