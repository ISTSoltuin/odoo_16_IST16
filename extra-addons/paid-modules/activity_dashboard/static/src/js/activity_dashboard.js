odoo.define('activity_dashboard.activity_dashboard', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var dialogs = require('web.view_dialogs');

    var ActivityDashboard = AbstractAction.extend({
        template: 'ActivityDashboard',

        events: {
            'click .btn-edit': '_onEdit',
            'click .btn-remove': '_onRemove'
        },

        _onEdit: function(ev) {
            ev.stopPropagation();
            var $element = $(ev.target);
            console.log($element)
            console.log($element.data('id'))
            return this.do_action({
                type: "ir.actions.act_window",
                res_model: 'mail.activity',
                domain: [],
                target: 'current',
                res_id: parseInt($element.data('id')),
                view_type: 'form',
                views: [[false, "form"]],
            });
        },

        _onRemove: function(ev) {
            var self = this;
            ev.stopPropagation();
            var $element = $(ev.target);
            console.log($element)
            console.log($element.data('id'))
            this._rpc({
                model: 'mail.activity',
                method: 'unlink',
                args: [parseInt($element.data('id'))],
            }).then(function () {
                self.load_data();
            });
        },

        init: function(parent, action) {
            this.params = action.params;
            this._super(parent, action);
        },
        
        start: function() {
            var self = this;
            self.load_data();
        },

        load_data: function () {
            var self = this;
            var existCondition = setInterval(function() {
                if ($('.o_view_controller').length) {
                    clearInterval(existCondition);
                    console.log("data : ", self)
                    
                    rpc.query({
                        model: 'dashboard.activity',
                        method: 'get_activities',
                        args: [],
                    }).then(function(result) {
                        console.log("dataaaaaa", result);
                        $('.o_view_controller').html(QWeb.render('ActivityDashboardContainer', {
                            'list_planned_activity': result['list_planned_activity'],
                            'list_today_activity': result['list_today_activity'],
                            'list_overdue_activity': result['list_overdue_activity'],
                        }));

                        $('#first-card-value').text(result['activities'][0]);
                        $('#second-card-value').text(result['activities'][1]);
                        $('#third-card-value').text(result['activities'][2]);
                        $('#fourth-card-value').text(result['activities'][3]);

                        var dataTables_buttons = [{
                            extend: 'collection',
                            text: '<img src="/activity_dashboard/static/src/assets/button-export.svg"> Export',
                            className: 'btn-export',
                            buttons: [
                                'excelHtml5',
                                'pdfHtml5',
                            ]
                        }];

                        self.$('table').DataTable({
                            "iDisplayLength": 5,
                            dom: 'Bfrtip',
                            buttons: dataTables_buttons, 
                        });


                    });
                }
            }, 500);
        },

    });

    core.action_registry.add("activity_dashboard", ActivityDashboard);
    return ActivityDashboard;

 });