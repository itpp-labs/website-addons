(function ($) {

    $.seedColors = function(seed){
        return $.seedColors.getColorBySeed(seed);
    };

    var $t = $.seedColors;

    $.extend($.seedColors, {
        settings: {
            color_bright_min: 50,
            color_diff: 20
        },
        getColorBySeed: function(seed){
            var $s = $t.settings;

            Math.seedrandom(seed);

            var brightCount = $t.randAB(1,3);

            var rgb = [];

            for (var i = 0; i < 3; i++) {

                if(brightCount > 0){
                    var c = $s.color_bright_min + $s.color_diff;
                    rgb[i] = $t.randAB(c * 4, 200);
                    brightCount--;
                    continue;
                }

                var c = $s.color_bright_min - $s.color_diff;
                rgb[i] = $t.randAB(0, c/10);
            }

            Math.seedrandom();

            return $t.getHtmlColor($t.getColorFromRGB(rgb));
        },
        randAB: function(min, max){
            return min + Math.round((max - min) * Math.random());
        },
        getColorFromRGB: function(rgb){
            return rgb[0] << 16 | rgb[1] << 8 | rgb[2] <<4;
        },
        getHtmlColor: function(color){
            return '#' + color.toString(16);
        }
    });

    $.fn.seedColors = function (action, options) {
        this.each(function () {
            var el = $(this);
            el.css("color", $.seedColors(el.html()));
        });
    };
})(jQuery);
