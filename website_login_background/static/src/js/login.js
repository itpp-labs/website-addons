$(document).ready(function () {
    if ($('.oe_website_login_container').length) {
        var height = $(window).innerHeight();
        var headerHeight = $('header').innerHeight();
        $('main').css('height', height);
        window.scrollTo(0, headerHeight);
    }
});


