function rnd_game() {
    openerp.jsonRpc("/chess/random_game/", 'call', {'status': true})
    .then(function (result) {console.log(result)});
};