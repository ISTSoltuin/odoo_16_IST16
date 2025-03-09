# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class SurveyTeam(models.Model):
    """Survey Team"""
    _name = 'survey.team'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = __doc__
    _rec_name = 'title'

    title = fields.Char(string="Title", required=True)
    employee_ids = fields.Many2many('res.users', string="Team Members")
    survey_project_id = fields.Many2one('project.project', readonly=True, store=True)
    survey_task_id = fields.Many2one('project.task', readonly=True, store=True)
    survey_manager_id = fields.Many2one('res.users', string="Project Manager", required=True)

    def create_survey_project(self):
        project_id = self.env['project.project'].sudo().create({
            'name': self.title,
            'user_id': self.survey_manager_id.id,
            'company_id': self.env.company.id,
        })
        self.survey_project_id = project_id.id
        return True
