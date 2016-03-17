function rnd_game() {
    var status = 1;
    openerp.session.rpc("/chess/random_game/", status);
};