# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class InstallationTeam(models.Model):
    """Installation Team"""
    _name = 'installation.team'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = __doc__
    _rec_name = 'installation_team'

    color = fields.Integer()
    installation_team = fields.Char(string="Installation Team", required=True)
    employee_ids = fields.Many2many('res.users', string="Team Members")

    installation_manager_id = fields.Many2one('res.users', string="Project Manager", required=True)
    project_installation_team_id = fields.Many2one('project.project', readonly=True, store=True, string="Installation Team")

    def create_project_installation_task(self):
        project_id = self.env['project.project'].sudo().create({
            'name': self.installation_team,
            'user_id': self.installation_manager_id.id,
            'company_id': self.env.company.id,
        })
        self.project_installation_team_id = project_id.id
        return True
