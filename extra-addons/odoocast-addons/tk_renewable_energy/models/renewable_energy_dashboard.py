# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class RenewableEnergyDashboard(models.Model):
    _name = "renewable.energy.dashboard"
    _description = "Renewable Energy Dashboard"

    @api.model
    def get_renewable_energy_dashboard(self):
        total_renewable_energy_order = self.env['renewable.energy.order'].sudo().search_count([])
        order_site_inspection = self.env['renewable.energy.order'].sudo().search_count(
            [('order_stages', '=', 'site_inspection')])
        material_order_stages = self.env['renewable.energy.order'].sudo().search_count(
            [('order_stages', '=', 'material_order')])
        material_arrived_stages = self.env['renewable.energy.order'].sudo().search_count(
            [('order_stages', '=', 'material_arrived')])
        project_installation_stages = self.env['renewable.energy.order'].sudo().search_count(
            [('order_stages', '=', 'project_installation')])
        qa_check_stages = self.env['renewable.energy.order'].sudo().search_count([('order_stages', '=', 'qa_check')])
        complete_stages = self.env['renewable.energy.order'].sudo().search_count([('order_stages', '=', 'complete')])

        survey_team_task = self.env['project.task'].sudo().search_count([('team_type', '=', 'survey_team')])
        installation_team_task = self.env['project.task'].sudo().search_count([('team_type', '=', 'installation_team')])
        qa_team_task = self.env['project.task'].sudo().search_count([('team_type', '=', 'qa_team')])

        total_order_count_graph = [['Total Orders', 'In Site Inspection', 'In Material Order', 'In Material Arrived',
                                    'In Project Installation', 'In QA Check', 'Completed'],
                                   [total_renewable_energy_order, order_site_inspection, material_order_stages,
                                    material_arrived_stages, project_installation_stages, qa_check_stages,
                                    complete_stages]]
        project_team_task = [['Survey Team', 'Installation Team', 'QA Team'],
                             [survey_team_task, installation_team_task, qa_team_task]]

        total_ren_lead = self.env['ren.lead'].sudo().search_count([])
        ren_lead_in_discussion = self.env['ren.lead'].sudo().search_count([('status', '=', 'b_in_discussion')])
        ren_lead_won = self.env['ren.lead'].sudo().search_count([('status', '=', 'c_won')])
        ren_lead_lost = self.env['ren.lead'].sudo().search_count([('status', '=', 'd_lost')])

        total_lead_status = [['Total', 'In Discussion', 'Won', 'Lost'],
                             [total_ren_lead, ren_lead_in_discussion, ren_lead_won, ren_lead_lost]]

        lead_source_phone_calls = self.env['ren.lead'].sudo().search_count([('lead_source_type', '=', 'phone_calls')])
        lead_source_e_mail = self.env['ren.lead'].sudo().search_count([('lead_source_type', '=', 'e_mail')])
        lead_source_social_media = self.env['ren.lead'].sudo().search_count([('lead_source_type', '=', 'social_media')])
        lead_source_website = self.env['ren.lead'].sudo().search_count([('lead_source_type', '=', 'website')])
        lead_source_direct_mail = self.env['ren.lead'].sudo().search_count([('lead_source_type', '=', 'direct_mail')])
        lead_source_events = self.env['ren.lead'].sudo().search_count([('lead_source_type', '=', 'events')])
        lead_source_public_relations = self.env['ren.lead'].sudo().search_count(
            [('lead_source_type', '=', 'public_relations')])
        lead_source_content_marketing = self.env['ren.lead'].sudo().search_count(
            [('lead_source_type', '=', 'content_marketing')])
        lead_source_branding = self.env['ren.lead'].sudo().search_count([('lead_source_type', '=', 'branding')])
        lead_source_online_marketing = self.env['ren.lead'].sudo().search_count(
            [('lead_source_type', '=', 'online_marketing')])
        lead_source_referrals = self.env['ren.lead'].sudo().search_count([('lead_source_type', '=', 'referrals')])

        lead_source_status = [
            ['Phone Calls', 'E-mail', 'Social Media', 'Website', 'Direct Mail', 'Events', 'Public Relations',
             'Content Marketing', 'Branding', 'Online Marketing', 'Referrals'],
            [lead_source_phone_calls, lead_source_e_mail, lead_source_social_media,
             lead_source_website, lead_source_direct_mail, lead_source_events, lead_source_public_relations,
             lead_source_content_marketing, lead_source_branding, lead_source_online_marketing, lead_source_referrals]]

        lead_customer_residential = self.env['ren.lead'].sudo().search_count(
            [('customer_category', '=', 'residential')])
        lead_customer_institutional = self.env['ren.lead'].sudo().search_count(
            [('customer_category', '=', 'institutional')])
        lead_customer_industrial = self.env['ren.lead'].sudo().search_count([('customer_category', '=', 'industrial')])
        lead_customer_commerical = self.env['ren.lead'].sudo().search_count([('customer_category', '=', 'commerical')])
        lead_customer_government = self.env['ren.lead'].sudo().search_count([('customer_category', '=', 'government')])
        lead_customer_social_sector = self.env['ren.lead'].sudo().search_count(
            [('customer_category', '=', 'social_sector')])

        lead_customer_category = [
            ['Residential', 'Institutional', 'Industrial', 'Commerical', 'Government', 'Social Sector'],
            [lead_customer_residential, lead_customer_institutional, lead_customer_industrial,
             lead_customer_commerical, lead_customer_government, lead_customer_social_sector]]

        data = {
            'total_renewable_energy_order': total_renewable_energy_order,
            'order_site_inspection': order_site_inspection,
            'material_order_stages': material_order_stages,
            'material_arrived_stages': material_arrived_stages,
            'project_installation_stages': project_installation_stages,
            'qa_check_stages': qa_check_stages,
            'complete_stages': complete_stages,
            'survey_team_task': survey_team_task,
            'installation_team_task': installation_team_task,
            'qa_team_task': qa_team_task,
            'total_order_count_graph': total_order_count_graph,
            'project_team_task': project_team_task,
            'total_lead_status': total_lead_status,
            'lead_source_status': lead_source_status,
            'lead_customer_category': lead_customer_category,
        }
        return data
