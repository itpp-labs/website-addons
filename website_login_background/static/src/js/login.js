$(document).ready(function () {
    if ($('.oe_website_login_container').length) {
        var headerHeight = $('header').innerHeight();
        window.scrollTo(0, headerHeight);
    }
});


