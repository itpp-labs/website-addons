/* Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html). */
odoo.define('website_multi_company_separate_orders', function(require) {
"use strict";

var session = require('web.session');
var sAnimations = require('website.content.snippets.animation');

sAnimations.registry.WebsiteSale.include({

    read_events: _.extend(sAnimations.registry.WebsiteSale.prototype.read_events, {
        'click td.td-product_name .separate_order:not(.child_order)': '_duplicate_order_request',
    }),

    _duplicate_order_request: function(event) {
        var cid = event.target.attributes.pcid.value;
        if (!cid) {
            return;
        }
        session.rpc("/shop/split_order_for_daughter_companies/" + cid, {})
            .then(function(result) {
                if (result) {
                    //        alert('Order was duplicated');
                    location.reload();
                }
            });
    },

});

});
