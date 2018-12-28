/* Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
   License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define('stock_picking_barcode.tour', function (require) {
    "use strict";

    var tour = require("web_tour.tour");
    var core = require('web.core');
    var _t = core._t;

    function open_inventory_ui() {
        return [{
            trigger: '.nav.navbar-nav.oe_application_menu_placeholder li:contains("Inventory") span',
            content: _t("Open inventory dashboard"),
        }, {
            trigger: 'div[name="stock_picking"]:contains("Receipts"):contains("YourCompany") .oe_stock_scan_image',
            content: _t("Click to launch the barcode interface"),
        }];
    }

    function add_product_by_barcode(barcode) {
        return [{
            content: 'dummy action',
//            trigger: '.text-left:contains("Product")',
            trigger: '.o_notification_manager',
            // 'run text' doesnt work for barcode simulating, it puts barcode string inside a selected element
            run: 'text ' + barcode,
        }, {
            content: 'check the product addition',
            extra_trigger: 'tr:contains("Ice Cream")',
            trigger: '.text-left:contains("Product")',
        }];
    }

    function add_product() {
        return [{
            content: 'increase quantity',
            trigger: 'tr .fa-plus',
        }, {
            content: 'check the product addition',
            trigger: 'tr .js_row_qty input[value="1"]',
        }];
    }

    var steps = [];
    steps = steps.concat(open_inventory_ui());
//    steps = steps.concat(add_product_by_barcode('0000000000017'));
    steps = steps.concat(add_product());

    tour.register('tour_stock_picking_barcode', { test: true, url: '/web' }, steps);

});
