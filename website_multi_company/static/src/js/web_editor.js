/* Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
   License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */
odoo.define('website_multi_company.web_editor', function (require) {
    'use strict';

    var ViewEditor = require('web_editor.ace');
    var weContext = require('web_editor.context');
    var session = require('web.session');

    var MultiViewEditor = ViewEditor.include({
        init: function () {
            this._super.apply(this, arguments);
            this.xmlDependencies.push('/website_multi_company/static/src/xml/web_editor.xml');
            this.events['click button[data-action="make-multi-website"]'] = '_onMakeMultiWebsiteClick';
        },
        start: function(){
            this.$makeMultiWebsite = this.$('[data-action="make-multi-website"]');
            this._super.apply(this, arguments);
        },
        _displayResource: function (resID, type) {
            this._super.apply(this, arguments);
            // button is visible in xml mode when debug is active and view is not multi-website yet
            var is_multi = this.resources['xml'][resID].name.indexOf('(Website #') !== -1;
            this.$makeMultiWebsite.toggleClass('hidden', is_multi || this.currentType === 'less' || !session.debug);
        },
        _onMakeMultiWebsiteClick: function(){
            var resID = this._getSelectedResource();
        },
        _makeMultiWebsite: function(resID){
            var esession = this.editingSessions['xml'][resID];
            this._rpc({
                model: 'ir.ui.view',
                method: 'make_multi_website',
                args: [[esession.id], weContext],
            }).then(function(){
                // save other changes and reload page
                return this._saveResources();
            }).bind(this);
        },
    });
    return MultiViewEditor;
});
