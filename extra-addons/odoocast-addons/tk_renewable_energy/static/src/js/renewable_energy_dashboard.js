odoo.define('tk_renewable_energy.RenewableEnergyDashboard', function (require) {
    'use strict';
    const AbstractAction = require('web.AbstractAction');
    const ajax = require('web.ajax');
    const core = require('web.core');
    const rpc = require('web.rpc');
    const session = require('web.session')
    const web_client = require('web.web_client');
    const _t = core._t;
    const QWeb = core.qweb;
    const { loadBundle } = require("@web/core/assets");

    const ActionMenu = AbstractAction.extend({
        template: 'renewable_energy_dashboard_template',
        events: {
            'click .total-renewable-energy-order': 'view_total_renewable_energy_order',
            'click .order-site-inspection': 'view_order_site_inspection',
            'click .material-order-stages': 'view_material_order_stages',
            'click .material-arrived-stages': 'view_material_arrived_stages',
            'click .project-installation-stages': 'view_project_installation_stages',
            'click .qa-check-stages': 'view_qa_check_stages',
            'click .complete-stages': 'view_complete_stages',
            'click .survey-team-task': 'view_survey_team_task',
            'click .installation-team-task': 'view_installation_team_task',
            'click .qa-team-task': 'view_qa_team_task',
        },

        renderElement: function (ev) {
            const self = this;
            $.when(this._super())
                .then(function (ev) {
                    rpc.query({
                        model: "renewable.energy.dashboard",
                        method: "get_renewable_energy_dashboard",
                    }).then(function (result) {
                        $('#total_renewable_energy_order').empty().append(result['total_renewable_energy_order']);
                        $('#order_site_inspection').empty().append(result['order_site_inspection']);
                        $('#material_order_stages').empty().append(result['material_order_stages']);
                        $('#material_arrived_stages').empty().append(result['material_arrived_stages']);
                        $('#project_installation_stages').empty().append(result['project_installation_stages']);
                        $('#qa_check_stages').empty().append(result['qa_check_stages']);
                        $('#complete_stages').empty().append(result['complete_stages']);
                        $('#survey_team_task').empty().append(result['survey_team_task']);
                        $('#installation_team_task').empty().append(result['installation_team_task']);
                        $('#qa_team_task').empty().append(result['qa_team_task']);
                        self.renOrderStatusGraph(result['total_order_count_graph']);
                        self.getProjectTeamTask(result['project_team_task']);
                        self.getTotalLeadStatus(result['total_lead_status']);
                        self.getLeadSourceStatus(result['lead_source_status']);
                        self.getLeadCustomerCategory(result['lead_customer_category']);
                    });
                });
        },

        view_total_renewable_energy_order : function (ev){
            ev.preventDefault();
            return this.do_action({
                name: _t('REN Orders'),
                type: 'ir.actions.act_window',
                res_model: 'renewable.energy.order',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form'], [false, 'calendar'], [false, 'activity']],
                target: 'current'
            });
        },
        view_order_site_inspection : function (ev){
            ev.preventDefault();
            return this.do_action({
                name: _t('Site Inspections'),
                type: 'ir.actions.act_window',
                domain: [['order_stages', '=', 'site_inspection']],
                res_model: 'renewable.energy.order',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form'], [false, 'calendar'], [false, 'activity']],
                target: 'current'
            });
        },
        view_material_order_stages : function (ev){
            ev.preventDefault();
            return this.do_action({
                name: _t('Materials Order'),
                type: 'ir.actions.act_window',
                domain: [['order_stages', '=', 'material_order']],
                res_model: 'renewable.energy.order',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form'], [false, 'calendar'], [false, 'activity']],
                target: 'current'
            });
        },
        view_material_arrived_stages : function (ev){
            ev.preventDefault();
            return this.do_action({
                name: _t('Materials Arrived'),
                type: 'ir.actions.act_window',
                domain: [['order_stages', '=', 'material_arrived']],
                res_model: 'renewable.energy.order',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form'], [false, 'calendar'], [false, 'activity']],
                target: 'current'
            });
        },
        view_project_installation_stages : function (ev){
            ev.preventDefault();
            return this.do_action({
                name: _t('Project Installations'),
                type: 'ir.actions.act_window',
                domain: [['order_stages', '=', 'project_installation']],
                res_model: 'renewable.energy.order',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form'], [false, 'calendar'], [false, 'activity']],
                target: 'current'
            });
        },
        view_qa_check_stages : function (ev){
            ev.preventDefault();
            return this.do_action({
                name: _t('QA Checks'),
                type: 'ir.actions.act_window',
                domain: [['order_stages', '=', 'qa_check']],
                res_model: 'renewable.energy.order',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form'], [false, 'calendar'], [false, 'activity']],
                target: 'current'
            });
        },
        view_complete_stages : function (ev){
            ev.preventDefault();
            return this.do_action({
                name: _t('Completes'),
                type: 'ir.actions.act_window',
                domain: [['order_stages', '=', 'complete']],
                res_model: 'renewable.energy.order',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form'], [false, 'calendar'], [false, 'activity']],
                target: 'current'
            });
        },
        view_survey_team_task : function (ev){
            ev.preventDefault();
            return this.do_action({
                name: _t('Survey Team Tasks'),
                type: 'ir.actions.act_window',
                domain: [['team_type', '=', 'survey_team']],
                res_model: 'project.task',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form'], [false, 'calendar'], [false, 'pivot'], [false, 'graph'], [false, 'activity']],
                target: 'current'
            });
        },
        view_installation_team_task : function (ev){
            ev.preventDefault();
            return this.do_action({
                name: _t('Installation Team Tasks'),
                type: 'ir.actions.act_window',
                domain: [['team_type', '=', 'installation_team']],
                res_model: 'project.task',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form'], [false, 'calendar'], [false, 'pivot'], [false, 'graph'], [false, 'activity']],
                target: 'current'
            });
        },
        view_qa_team_task : function (ev){
            ev.preventDefault();
            return this.do_action({
                name: _t('QA Team Tasks'),
                type: 'ir.actions.act_window',
                domain: [['team_type', '=', 'qa_team']],
                res_model: 'project.task',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form'], [false, 'calendar'], [false, 'pivot'], [false, 'graph'], [false, 'activity']],
                target: 'current'
            });
        },

        get_action: function (ev, name, res_model){
            ev.preventDefault();
            return this.do_action({
                name: _t(name),
                type: 'ir.actions.act_window',
                res_model: res_model,
                views: [[false, 'kanban'],[false, 'tree'],[false, 'form']],
                target: 'current'
            });
        },

        apexGraph: function () {
            Apex.grid = {
                padding: {
                    right: 0,
                    left: 0,
                    top: 10,
                }
            }
            Apex.dataLabels = {
                enabled: false
            }
        },

        renOrderStatusGraph: function(data){
        const options = {
          series: [
            {
            name: 'Orders',
            data: data[1]
            }
          ],
        chart: {
          height: 400,
          type: 'bar',
        },
        colors: ['#f29e4c', '#f1c453', '#efea5a',  '#b9e769',  '#83e377', '#16db93', '#0db39e', '#048ba8', '#2c699a', '#54478c'],
        plotOptions: {
          bar: {
            columnWidth: '10%',
            distributed: true,
          }
        },
        dataLabels: {
          enabled: false
        },
        legend: {
          show: false
        },
        xaxis: {
            categories: data[0],
            labels: {
                style: {
                    colors: ['#f29e4c', '#f1c453', '#efea5a',  '#b9e769',  '#83e377', '#16db93', '#0db39e', '#048ba8', '#2c699a', '#54478c'],
                    fontSize: '12px'}
            }
        }
        };
        this.renderGraph("#ren_order_status", options);
        },

        getProjectTeamTask: function(data){
          const options = {
            series: data[1],
            chart: {
            width: 500,
            height: 500,
            type: 'polarArea',
          },
          yaxis: {
        labels: {
              formatter: function (val) {
                return val.toFixed(0);
              }
            },
        },
          labels: data[0],
          stroke: {
            colors: ['#fff']
          },
          fill: {
            opacity: 0.8
          },
          responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                  width: 200
                },
                legend: {
                  position: 'bottom'
                }
            }
        }]
        };
        this.renderGraph("#project_team_task", options);
        },

        getTotalLeadStatus: function(data){
          const options = {
            series: data[1],
            chart: {
            width: 500,
            height: 500,
            type: 'polarArea',
          },
          yaxis: {
        labels: {
              formatter: function (val) {
                return val.toFixed(0);
              }
            },
        },
          labels: data[0],
          stroke: {
            colors: ['#fff']
          },
          fill: {
            opacity: 0.8
          },
          responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                  width: 200
                },
                legend: {
                  position: 'bottom'
                }
            }
        }]
        };
        this.renderGraph("#total_lead_status", options);
        },

        getLeadSourceStatus: function(data){
          const options = {
            series: data[1],
            chart: {
            width: 500,
            height: 500,
            type: 'polarArea',
          },
          yaxis: {
        labels: {
              formatter: function (val) {
                return val.toFixed(0);
              }
            },
        },
          labels: data[0],
          stroke: {
            colors: ['#fff']
          },
          fill: {
            opacity: 0.8
          },
          responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                  width: 200
                },
                legend: {
                  position: 'bottom'
                }
            }
        }]
        };
        this.renderGraph("#lead_source_status", options);
        },

        getLeadCustomerCategory: function(data){
          const options = {
            series: data[1],
            chart: {
            width: 500,
            height: 500,
            type: 'polarArea',
          },
          yaxis: {
        labels: {
              formatter: function (val) {
                return val.toFixed(0);
              }
            },
        },
          labels: data[0],
          stroke: {
            colors: ['#fff']
          },
          fill: {
            opacity: 0.8
          },
          responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                  width: 200
                },
                legend: {
                  position: 'bottom'
                }
            }
        }]
        };
        this.renderGraph("#lead_customer_category", options);
        },

        renderGraph: function(render_id, options){
           $(render_id).empty();
           const graphData = new ApexCharts(document.querySelector(render_id), options);
           graphData.render();
        },

        willStart: function () {
            const self = this;
            self.drpdn_show = false;
            return Promise.all([loadBundle(this), this._super()]);
        },
    });
    core.action_registry.add('renewable_energy_dashboard', ActionMenu);
});
