$(document).ready(function() {
    "use strict";
    if (!$("#cart_products")) {
        return;
    }

    var input_selector = "input[data-product-id]";

    function check(el) {
        if (!el) {
            el = input_selector;
        }

        var available = true;
        $(el).each(function() {
            var quantity = parseInt($(this).val(), 10);
            var $tr = $(this)
                .parent()
                .parent()
                .parent();
            var virtual_available = parseInt(
                $tr.find('[name="virtual_available"]').text(),
                10
            );
            var enough = quantity <= virtual_available;
            $tr.toggleClass("warning", !enough);
            if (!enough) {
                available = false;
            }
        });
        $('a[href$="/shop/checkout"]').toggleClass("disabled", !available);
    }

    $(input_selector).on("change", function() {
        check(this);
    });

    check();
});
