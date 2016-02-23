$(document).ready(function () {
    $('.oe_website_sale .a-submit-buy-now').off('click').on('click', function () {
        $(this).closest('form').find('input[name="buy_now"]').val(1)
        $(this).closest('form').submit();
    });

})
