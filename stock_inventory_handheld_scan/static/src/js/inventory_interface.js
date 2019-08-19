/* Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */
odoo.define('stock_inventory_handheld_scan.widget', function (require) {
"use strict";

var FormController = require('web.FormController');
var ListRenderer = require('web.ListRenderer');
var core = require('web.core');
var QWeb = core.qweb;

var rpc = require('web.rpc');

ListRenderer.include({
    _renderRow: function (record) {
        var res = this._super(record);
        if (this.state.model === "stock.inventory.line") {
            res.attr('line_id', record.data.id)
        }
        return res;
    },
});

FormController.include({

    renderButtons: function ($node) {
        var self = this;
        var result = this._super.apply(this, arguments);
        if (this.modelName === "stock.inventory" && this.mode !== 'edit') {
            this.scan_button = this.create_stock_scan_modal(this.$buttons);
            $('.o_main').addClass('inventory_adjustment_extension');
        }
        return result;
    },

    check_barcode: function (barcode) {
        var self = this;
        var inv_id = this.initialState.data.id;
        return rpc.query({
            model: 'stock.inventory',
            method: 'action_check_barcode',
            args: [[inv_id], barcode],
        }).then(function(res){
            self.modal.data = res;
            if (res && res.product_id) {
                if (res.line_id) {
                    self.update_result_panel(res);
                    return;
                }
//                if (self.check_product_presence(res)){
//                    self.update_result_panel(res);
//                    return;
//                }
                self.update_result_panel(_.extend(res || {}, {message: 'This product is not in the adjustment'}));
                return;
            }
            self.update_result_panel(_.extend(res || {}, {message: 'This barcode does not exist'}));
        });
    },

//    check_product_presence: function (data) {
//        var lines = this.initialState.data.line_ids.data;
//        if (!lines) {
//            return false;
//        }
//        var products = _.filter(lines, function(line) {
//            return line.data.product_id.data.id === data.product_id;
//        });
//        if (products && products.length) {
//            this.modal_products = products;
//            return true;
//        }
//        return false;
//    },

    shallowly_update_tree_view: function(data, val) {
        $('.o_data_row.text-info[line_id='+ data.line_id + '] .o_list_number:last').val(val);
        $('.o_data_row.text-info[line_id='+ data.line_id + '] .o_list_number:last').text(val);
        console.log(data);
    },

    update_result_panel: function (data) {
        var self = this;
        this.modal.find('.panel-heading').hide();
        var result_panel = this.modal.find('.panel-hidden');
        if (data && data.message) {
            result_panel.find('.message').text(data.message);
            result_panel.find('.message-container').show();
            return;
        }
        _.chain(data).
            keys().
            each(function(k) {
                result_panel.find('.' + k).text(data[k]);
            });
        result_panel.find('.product_qty').val(parseInt(data.product_qty));
        result_panel.find('.data-container').show();
        var update_qty_btn = this.modal.find('.update_qty');
        var input = this.modal.find('.product_qty');
        update_qty_btn[0].style.display = 'inline';
        result_panel.show();
        input.focus();
        update_qty_btn.on('click', function (e) {
            var val = parseInt(input.val());
            if (val && val !== self.modal.data.product_qty) {
                self.shallowly_update_tree_view(data, val);
                self.update_qty_in_inventory(val);
            }
            self.destroy_stock_modal();
        });
    },

    update_qty_in_inventory: function (qty) {
        return rpc.query({
            model: 'stock.inventory.line',
            method: 'action_update_inventory_line_qty',
            args: [[this.modal.data.line_id], qty],
        }).then(function(res){
//            location.reload();
        });
    },

    create_stock_scan_modal: function (node) {
        var self = this;
        var button_xml = '<button class="btn btn-sm btn-default oe_highlight" data-original-title="" id="action_scan_barcode">Scan</button>'
        node.find('.o_form_buttons_view').append(button_xml);

        var result = node.find('#action_scan_barcode');
        result.on('click', function(e){
            self.open_stock_scan_modal();
        });
        return result;
    },

    open_stock_scan_modal: function () {
        var self = this;
        var modal_xml = $(QWeb.render('stock_scan_modal', {}));
        $('.o_web_client').append(modal_xml);
        var modal = $('#stock_scan_modal');
        this.modal = modal;
        modal.find('.close-btn').on('click', function(e){
           self.destroy_stock_modal();
        });
        modal.show();
        var input = modal.find('.hidden_barcode_input input');
        input.focus();
        var check_barcode_button = $('.check-barcode');
        check_barcode_button.on('click', function(){
            self.check_barcode(input.val);
        });
        input.on('change', function(e) {
            check_barcode_button.off();
            var value = e.currentTarget.value;
            if (value) {
                self.check_barcode(e.currentTarget.value);
            }
            e.currentTarget.value = '';
        });
        input.on('keyup', function(e) {
            self.timeout = setTimeout(function () {
                check_barcode_button.click();
            }, 1000);
        });
    },

    destroy_stock_modal: function(){
        this.modal.remove();
    },
});

});
