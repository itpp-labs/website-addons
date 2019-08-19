/* Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */
odoo.define('stock_inventory_handheld_scan.widget', function (require) {
"use strict";

var FormController = require('web.FormController');

var core = require('web.core');
var QWeb = core.qweb;

var rpc = require('web.rpc');

FormController.include({

    renderButtons: function ($node) {
        var self = this;
        var result = this._super.apply(this, arguments);
        if (this.modelName === "stock.inventory"  && this.mode !== 'edit') {
            this.create_stock_scan_modal(this.$buttons);
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
                self.update_result_panel(_.extend(res || {}, {message: 'This product is not in the adjustment'}));
                return;
            }
            self.update_result_panel(_.extend(res || {}, {message: 'This barcode does not exist'}));
        });
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
            location.reload();
        });
    },

    create_stock_scan_modal: function (node) {
        var self = this;
        var button_xml = '<button class="btn btn-sm btn-default oe_highlight" data-original-title="" id="action_scan_barcode" title="">Scan</button>'
        node.find('.o_form_buttons_view').append(button_xml);

        node.find('#action_scan_barcode').on('click', function(e){
            self.open_stock_scan_modal();
        });
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
        input.on('change', function(e) {
            var value = e.currentTarget.value;
            if (value) {
                self.check_barcode(e.currentTarget.value);
            }
            e.currentTarget.value = '';
        });
    },

    destroy_stock_modal: function(){
        this.modal.remove();
    },
});

});
