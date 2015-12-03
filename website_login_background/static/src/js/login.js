$(document).ready(function () {
    var height = $(window).innerHeight();
    var headerHeight = $('header').innerHeight();
    $('main').css('height', height);
    window.scrollTo(0, headerHeight);
});


