# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class QaTeam(models.Model):
    """Qa Team"""
    _name = 'qa.team'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = __doc__
    _rec_name = 'title'

    title = fields.Char(string="Title", required=True)
    employee_ids = fields.Many2many('res.users', string="Team Members")
    qa_team_project_id = fields.Many2one('project.project', readonly=True, store=True)
    qa_manager_id = fields.Many2one('res.users', string="Project Manager", required=True)


    def create_qa_team_project(self):
        project_id = self.env['project.project'].sudo().create({
            'name': self.title,
            'user_id': self.qa_manager_id.id,
            'company_id': self.env.company.id,
        })
        self.qa_team_project_id = project_id.id
        return True
