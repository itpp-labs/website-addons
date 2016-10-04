=======
 Chess
=======

Installation
============

For Odoo 8

Usage
=====

**New game**

* 1 Click to "Chess" in the main menu of the site

  * 1.1 Create game - in this regime an invitation to the game is sent to a registered on the site random player.
  * 1.2 Play with a friend - this regime allows to choose person to whom invitation will be sent.

* 2 Choose the game settings

  * 2.1 Indicate Game type. Standart - game goes without time restrictions. Blitz - with the fixed time in game. Limited time - with the fixed time in move. When choosing  Blitz or Limited time, field Time opens and indicates a time in appropriate styles. D- time in days, H – time on clocks, M – time in minutes, s – time in seconds. (Default time is 15 minutes)
  * 2.2 Choose Figure color
  * 2.3 Press "Create game". Game will start when the second player accepts an invitation.

**Invitation**

* 1 Open Chess in the menu.

  * 1.1 Click New games. You will see invitations list from other players.

    * 1.1.1 Click in Accept a new page will be opened and game will be started.
    * 1.1.2 Click in Refuse - is reject from the game, a note will be transferred to Refusals of games.

  * 1.2 Click Activegames. You will see active games list. You can start the game by clicking in Go to the game.
  * 1.3 Click Completedgames – a list of completed games.
  * 1.4 Click My invitations – invitations list, which were sent by you. When clicking to cancel you cancel the invitation.
  * 1.5 Click Refusals of games – invitations list to the game, players of which refused to accept the game.
  * 1.6 Click Canceled games – list of canceled invitations.

**Game**

* 1 Press the left button of a computer mouse and keep it pressed to move the figure to right place.

  * 1.1 Press to PGN in the right of chessboard  to view done move.

* 2 Click Surrender to give up.
* 3 Click Sugest a draw to offer a draw to your opponent.
* 4 Click the settings to watch FEN and change the orientation of the chess board.
* 5 Put “V” to Windowchat to open chat.
* 6 Write a message to chat and send it by clicking to send or with the help of ctrl + enter.

**End of the game**

End of the game is determined by game rules or by such possible actions of players as:

* 1 draw after 50 moves.
* 2 Rule of 3 repetitions.
* 4 Auto draw  because of the lack of the figures for checkmate.
* 5 One of the players gave up.
* 6 One of the players accepted draw.
* 7 One of the players was over time.

**Results of a game**

Result of a game is player’s new rating, which is calculated according to Elo system and is written of the left of chess board.

**Note.** To use the module, you need to be sure that your odoo instance support longpolling, i.e. Instant Messaging works.
Read more about how to use the `longpolling  <https://odoo-development.readthedocs.io/en/latest/admin/longpolling.html>`__
