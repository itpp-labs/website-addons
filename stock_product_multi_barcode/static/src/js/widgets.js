/* Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */
odoo.define('stock_product_multi_barcode.widget', function (require) {
"use strict";

var core = require('web.core');
var rpc = require('web.rpc');
var stock_widgets = require('stock_picking_barcode.widgets');

var _t = core._t;
var qweb = core.qweb;

console.log(core.action_registry)
console.log(stock_widgets)
console.log(stock_widgets)

stock_widgets.PickingMainWidget.include({

    load: function(picking_id) {
        var self = this;
        var result = this._super.apply(this, arguments);

        return result.then(function(res){
            var product_ids = _.uniq(_.map(self.packoplines, function(line) {
                return line.product_id[0]
            }));
            return rpc.query({
                model: 'res.partner.product.barcode',
                method: 'search_read',
                fields: ['id', 'barcode', 'product_id', 'partner_id'],
                domain: [
                    ['product_id', 'in', product_ids],
                ],
            }).then(function(vendor_barcodes){
                var lines = false;
                 _.each(self.packoplines, function(line){
                    if (line.product_barcode) {
                        if (typeof line.product_barcode === 'string'){
                            line.product_barcode = [line.product_barcode];
                        }
                    } else {
                        line.product_barcode = []
                    };
                });
                _.each(vendor_barcodes, function(bar) {
                    lines = _.filter(self.packoplines, function(line){
                        return line.product_id[0] === bar.product_id[0];
                    });
                    _.each(lines, function(line){
                        line.product_barcode.push(bar.barcode);
                    });

                });
            });
        });
    },

    _barcode_handler: function(barcode){
        var self = this;
        var lines = _.filter(this.packoplines, function(l) {
            return _.contains(l.product_barcode, barcode);
        });
        if (lines.length > 1) {
            return $('#js_multiple_products').modal();
        }
        return this._super.apply(this, arguments);
    },

});

});
