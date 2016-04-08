/*create game (time)*/
$('#create_game #blitz, #play_with_a_friend #blitz').click(function(){
    $('#create_game #time').show();
    $('#play_with_a_friend #time').show();
});
$('#create_game .limited_time, #play_with_a_friend .limited_time').click(function(){
    $('#create_game #time').show();
    $('#play_with_a_friend #time').show();
});
$('#create_game #standart, #play_with_a_friend #standart').click(function(){
    $('#create_game #time').hide();
    $('#play_with_a_friend #time').hide();
});