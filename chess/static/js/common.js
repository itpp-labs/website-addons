var init = function() {
//--- start ---
  var other_user='';
  var this_user='';
  
  var other_user_draw=false;
  var this_user_draw=false;
  
  var other_user_surrender=false;
  var this_user_surrender=false;
  
  other_user=true; //for example
  
  var board,
  game = new Chess(),
  statusEl = $('#status'),
  fenEl = $('#fen'),
  pgnEl = $('#pgn'),
  DelWEl = $('#figure_white'),
  DelBEl = $('#figure_black'),
  /*some figures were removed*/
  OLD_FEN_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
  lenOldFen = ((OLD_FEN_POSITION.split('/')).join('')).replace(/[0-9]/g, '').length,
  pos = [];
  pgnEl.on('click', 'a',function(event) {
	event.preventDefault();
	var data = $(this).data('move').split(',');
	var i = $(this).index();
	board.position(pos[i],false);
	board.move.apply(null,data);
  })

  var onDragStart = function(source, piece, position, orientation) {
    board.position(game.fen());
    if (game.game_over() === true ||
      (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
	//(orientation === 'white' && piece.search(/^b/) !== -1) ||
    //(orientation === 'black' && piece.search(/^w/) !== -1)) {
    return false;
    }
  };

  var onDrop = function(source, target) {
  // see if the move is legal
    var move = game.move({
      from: source,
      to: target,
      promotion: 'q'	  // NOTE: always promote to a queen for example simplicity
    });
 
  // illegal move
    if (move === null) return 'snapback';
	else {
	  console.log("Source: " + source);
	  console.log("Target: " + target);
	  console.log("Move: " + source+"-"+target);
	  console.log("____________________________");
	}
	onDelFigure()
    updateStatus();
	
  };
  
    $('#moveBtn').on('click', function() {
	onDrop('e2', 'e4');
	onSnapEnd();
  });
  
  var onDelFigure = function() {
	  	  
	  /* It is only important as a shortened post we will use
	  only to determine the remote pieces on the board */
	  
	  NewFenPosition = (game.fen()).split(' ');
	  OldFenPosition =((OLD_FEN_POSITION.split('/')).join('')).replace(/[0-9]/g, ''),
	  NewFenPosition = ((NewFenPosition[0].split('/')).join('')).replace(/[0-9]/g, '');
	  var oldArr = (OldFenPosition.split('')).sort(),
	      newArr = (NewFenPosition.split('')).sort();
	  OldFenPosition = oldArr.join('');
	  NewFenPosition = newArr.join('');
	  
	  /*if not the same as the length of the old with the new, then removed figure*/
	  if (lenOldFen != NewFenPosition.length)
	  {
		
		var WhiteArr=[], BlackArr=[];
		var pattern = /[A-Z]/;
		for (var i = 0; i < oldArr.length; i++)
		{
			var elem = oldArr[i];
			var index = newArr.indexOf(elem);
			if ( index != -1){
				newArr.splice(index,1);	
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
			DelWEl.html(DelWF);			
		};
		
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
			DelBEl.html(DelBF);		
		}
		
		lenOldFen=lenOldFen-1;
	  }		
  }


// update the board position after the piece snap 
// for castling, en passant, pawn promotion
  var onSnapEnd = function() {
    board.position(game.fen());
  };

  var updateStatus = function() {
    var status = '';

    var moveColor = 'White';
    if (game.turn() === 'b') {
      moveColor = 'Black';
    }
  
    var typea="success",
    check="";
    if(moveColor=="White") {
      typea="warning";
    }

    
  
  // checkmate?
    if (game.in_checkmate() === true) {
      status = moveColor + ' is in checkmate.';
      swal({
        title : "Game Over",
        text : moveColor+" is in checkmate.",
        type : typea,
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",   
        confirmButtonText: "New game",
	    cancelButtonText: "Close",
	    closeOnConfirm: false,
	    closeOnCancel: false
	  },
	
	  function(isConfirm){   
	  if (isConfirm && other_user==true) {
		  this_user = true;
		  swal("New game", "Click OK to continue", "success");   
		  board.destroy();
		  $(document).ready(init);
		  } else if (isConfirm && other_user=='') {
			  this_user = true;
			  swal("Wait please", "The user has not taken a decision", "success");  
		  } else {     
		  this_user = false;
		  swal("Cancelled", "Game over", "error");
		  game.game_over();
		  }
      });
    }
  
  
  // draw?
    else if (game.in_draw() === true) {
      status = 'Game over, drawn position';
      swal({
        title : "Game Over",
        text : "Drawn position.",
        type : typea,
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",   
        confirmButtonText: "New game",
	    cancelButtonText: "Close",
	    closeOnConfirm: false,
	    closeOnCancel: false
	  },
	
	    function(isConfirm){   
	    if (isConfirm && other_user==true) {
		    this_user = true;
		    swal("New game", "Click OK to continue", "success");   
		    board.destroy();
		    $(document).ready(init);
		    } else if (isConfirm && other_user=='') {
			    this_user = true;
			    swal("Wait please", "The user has not taken a decision", "success");  
		    } else {     
		    this_user = false;
		    swal("Cancelled", "Game over", "error");
		    game.game_over();
		    }
        });
      }
  
  // game still on
      else {
        status = moveColor + ' to move';

    // check?
        if (game.in_check() === true) {
          status += ', ' + moveColor + ' is in check';
	      swal({   title: moveColor + ' is in check',   text: moveColor + ' to move',   timer: 1000,   showConfirmButton: false });
        }
      }	
  
      pos.push(game.fen());
      statusEl.html(status);
      fenEl.html(game.fen());
      pgnEl.html(game.pgn());
    };
	
	
  var cfg = {
    moveSpeed: 'slow',
    snapbackSpeed: 500,
    snapSpeed: 100,
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd
  };

// surrender?
  $('#surrender').click(function(){
	swal({   
	  title: "Are you sure?",   
	  text: "You will lose",   
	  type: "warning",   
	  showCancelButton: true,   
	  confirmButtonColor: "#DD6B55",   
	  confirmButtonText: "Yes",   
	  cancelButtonText: "No",   
	  closeOnConfirm: false}, 
	  function(isConfirm){   
	    if (isConfirm) {     
		  swal({title: "Game over", text: 'You lose',   timer: 2000, type: "error", showConfirmButton: false });
		  this_user_surrender=true;
		  status = 'Game over, you lose';
		  compelled_game_over(status);
		}
		$('#surrender').hide();
		
	  });
  });

  if (other_user_surrender==true) {
	swal("You win!", "Another user surrendered", "success");
	status = 'Game over, you win!';
	compelled_game_over(status);
  };

  // suggest a draw?
  $('#suggest_a_draw').click(function(){
    swal({
	  title: "Are you sure?",   
	  text: "Send a message to offer a draw",   
	  type: "warning",   
	  showCancelButton: true,   
	  confirmButtonColor: "#DD6B55",   
	  confirmButtonText: "Yes",   
	  cancelButtonText: "No",   
	  closeOnConfirm: false },
	  function(isConfirm){   
	    if (isConfirm) {     
		  swal({
			title: 'Message sent',   
			text: 'Wait for an answer from another user',   
			timer: 2000,   
			showConfirmButton: false 
			});
		  this_user_draw=true;
		  $('#suggest_a_draw').hide();
		  
		}
	  });
  });
  
  if (other_user_draw==true && this_user_draw==false) {
    swal({
    title: "Draw",   
    text: "Another user offers a draw!",   
    type: "warning",   
    showCancelButton: true,   
    confirmButtonColor: "#DD6B55",   
    confirmButtonText: "To accept",   
    cancelButtonText: "Refuse",   
    closeOnConfirm: false },
    function(isConfirm){   
	  if (isConfirm) {
	    this_user_draw = true;
	    swal("Game over", "in a draw", "success");
	    status = 'Game over in a draw';
	    compelled_game_over(status);
	  }
    });
  } else if (other_user_draw && this_user_draw) {
	  swal("Game over", "in a draw", "success");
	  status = 'Game over in a draw';
	  compelled_game_over(status);
  };

  
  var board = ChessBoard('board', cfg);
  $('#flipOrientationBtn').on('click', board.flip);
  updateStatus();

  function compelled_game_over(status){
	statusEl.html(status);
	var cfg = {
	  moveSpeed: 'slow',
	  snapbackSpeed: 500,
	  snapSpeed: 100,
	  position: game.fen(),
	};
  board = ChessBoard('board', cfg);
  $('#flipOrientationBtn').on('click', board.flip);
  };
}; 

window.onload= function() {
  document.getElementById('toggler').onclick = function() {
	  openbox('box', this);
	  return false;
  };
	document.getElementById('cancel_game').onclick = function() {
		swal({   title: 'Warnning',   text: 'Game canceled',   timer: 2000,   showConfirmButton: false });
  		var board = ChessBoard('board', 'start');
  		$('#cancel_game').hide();
  		$('.canceled').show();
		$('#surrender').hide();
		$('#suggest_a_draw').hide();
		$('#toggler').hide();
		$('#box').hide();
	};
};
function openbox(id, toggler) {
  var div = document.getElementById(id);
	if(div.style.display == 'block') {
	  div.style.display = 'none';
	  toggler.innerHTML = 'Setting';
	}
	else {
	  div.style.display = 'block';
	  toggler.innerHTML = 'Close';
	}
}
function func_hide_chat() {
    if (document.getElementById("toggle_chat").checked) {
        $('.chat').show();
    }
    else {
		$('.chat').hide();
    }
}
$(document).ready(init);