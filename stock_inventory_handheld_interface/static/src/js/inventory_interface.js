/* Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */
odoo.define('stock_inventory_handheld_interface.widget', function (require) {
"use strict";

var FormRenderer = require('web.FormRenderer');

var core = require('web.core');
var QWeb = core.qweb;

var rpc = require('web.rpc');

FormRenderer.include({

    _renderHeaderButtons: function (node) {
        var self = this;
        var result = this._super.apply(this, arguments);
        var state = this.state;
        if (state.model === "stock.inventory" && state.data.state === "confirm" && this.mode !== 'edit') {
            this.create_stock_modal(result);
        }
        return result;
    },

    create_stock_modal: function(button_box){
        var self = this;
        var button_xml = '<button class="btn btn-sm btn-default oe_highlight" data-original-title="" id="action_scan_inventory" title="">Scan Inventory</button>'
        button_box.append(button_xml);

        button_box.find('#action_scan_inventory').on('click', function(e){
            var state = self.state;
            if (!state.data.line_ids.data.length){
                return;
            }
            var modal_xml = $(QWeb.render('action_scan_inventory_modal', {
                                state:state,
                                line: state.data.line_ids.data[0],
                            }));
            $('.o_web_client').append(modal_xml);
            var modal = $('#action_scan_inventory_modal');
            modal.state = state;
            self.update_stock_modal(modal);
            modal.render_header();
            var line = modal.current_line.data;
            if (line.theoretical_qty === line.product_qty) {
                modal.modal_skip_product();
            }
        });
    },

    update_stock_modal: function(modal){
        var self = this;
        this.modal = modal;
        var state = modal.state;

        modal.current_line = state.data.line_ids.data[0];
        modal.current_line_ind = 0;
        modal.lines = _.filter(state.data.line_ids.data, function(l){
            return l.data.theoretical_qty !== l.data.product_qty;
        });
        modal.updated_lines = [];

        modal.show();
        modal.render_header = function(options){
            if (options && options.message) {
                modal.find('.panel-heading').html(options.message);
                modal.find('.panel-content').hide();
                return;
            }
            if (!modal.lines.length) {
                modal.find('.panel-heading').html('There are no lines to scan');
                modal.find('.panel-content').hide();
                modal.find('.panel-footer').hide();
                return;
            }
            var line = modal.current_line.data;
            modal.find('.item2').text(line.product_id.data.display_name);
            modal.find('.size2').text(line.product_uom_id.data.display_name);
            modal.find('.qty2').text(line.theoretical_qty);
            modal.find('.modal_input').val(modal.current_line.data.product_qty || '');
        };


        modal.modal_check_barcode = function(){
            self.create_check_barcode_modal();
        };

        modal.modal_update_qty = function(){
            var line = modal.current_line;
            line.data.product_qty = modal.product_qty || line.data.product_qty || 0;
            var already_updated_line = _.find(modal.updated_lines, function(l){
                return l.data.id === line.data.id;
            });
            if (already_updated_line) {
                already_updated_line = line;
            } else {
                modal.updated_lines.push(line);
            }
            if (parseInt(line.data.product_qty) === parseInt(line.data.theoretical_qty)) {
                modal.lines.splice(modal.current_line_ind, 1);
            }
            modal.select_next_product();
        };

        modal.set_product_qty = function(e) {
            modal.product_qty = e.target.value;
        }

        modal.modal_skip_product = function(){
            modal.product_qty = 0;
            modal.select_next_product();
        };

        modal.select_next_product = function() {
            modal.current_line_ind = modal.lines[modal.current_line_ind + 1]
            ? modal.current_line_ind + 1
            : 0;
            modal.current_line = modal.lines[modal.current_line_ind];
            if (modal.current_line) {
                modal.product_qty = modal.current_line.data.product_qty || 0;
                modal.render_header();
            } else {
                modal.render_header({
                    message: 'Lines are over please click "Save & Exit"'
                });
            }
        };

        modal.exit = function(){
            self.destroy_stock_modal();
        };

        modal.modal_save_exit = function(){
            if (!modal.updated_lines.length) {
                modal.exit();
                return;
            }
            self.save_handheld_inventory().done(function(data){
                // TODO: maybe smth with data
                modal.exit();
                location.reload();
            });
        };

        modal.find('button.modal_check_barcode').on('click', modal.modal_check_barcode);
        modal.find('button.modal_update_qty').on('click', modal.modal_update_qty);
        modal.find('button.modal_skip_product').on('click', modal.modal_skip_product);
        modal.find('button.modal_save_exit').on('click', modal.modal_save_exit);
        modal.find('span.close').on('click', modal.exit);

        modal.find('input.modal_input').on('change', modal.set_product_qty);

        return modal;
    },

    save_handheld_inventory: function() {
        var modal = this.modal;
        var lines = [];
        _.each(modal.updated_lines, function(line) {
            lines.push({
                'product_qty': line.data.product_qty,
                'res_id': line.res_id,
            });
        });
        return rpc.query({
                model: 'stock.inventory',
                method: 'action_done_by_handheld',
                args: [modal.state.data.id, lines]
            });
    },

    destroy_stock_modal: function(){
        this.modal.remove();
    },

    create_check_barcode_modal: function(){
        var self = this;

        var loaded_barcodes = $.Deferred();
        var barcode = rpc.query({
                model: 'product.product',
                method: 'search_read',
                args: [[['id', '=', self.modal.current_line.data.product_id.data.id]], ['barcode']]
            }).then(function(res){
                var default_barcode = self.modal.current_line.data.product_barcode;
                self.modal.current_line.data.product_barcode = default_barcode || res[0].barcode;

                rpc.query({
                    model: 'res.partner.product.barcode',
                    method: 'search_read',
                    args: [[['product_id', '=', self.modal.current_line.data.product_id.data.id]], ['barcode', 'id']]
                }).then(function(res){
                    loaded_barcodes.resolve(res);
                });
            });
        var check_barcode_modal_xml = $(QWeb.render('check_barcode_modal', {
                                            line: this.modal.current_line,
                                        }));
        $('.o_web_client').append(check_barcode_modal_xml);
        var check_barcode_modal = $('#check_barcode_modal');
        check_barcode_modal.find('.check_barcode_input').focus().on('change', function(e){
            var barcodes = self.modal.vendor_barcodes || [];
            if (this.value &&
                this.value === self.modal.current_line.data.product_barcode ||
                _.contains(barcodes, this.value)) {
                $('#check_barcode_modal .panel-message').html('Barcodes are matched');
            } else {
                $('#check_barcode_modal .panel-message').html('Incorrect Barcode Scanned');
            }
        });
        check_barcode_modal.find('.check_barcode_modal_exit').on('click', function(){
            check_barcode_modal.remove();
        });

        return loaded_barcodes.then(function(res){
            self.modal.vendor_barcodes = _.pluck(res, 'barcode');
            check_barcode_modal.show();
            var text = self.modal.current_line.data.product_barcode && self.modal.current_line.data.product_barcode || '';
            text = text + ',' + (self.modal.vendor_barcodes.length && self.modal.vendor_barcodes || '');
            $('.barcode2').text(text);
            $('#check_barcode_modal .check_barcode_input').focus();
        });
    },

});

});
