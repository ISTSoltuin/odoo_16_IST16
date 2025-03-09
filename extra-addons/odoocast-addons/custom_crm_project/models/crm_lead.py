# Copyright @ODOOCAST 2024 contato@odoocast.com.br
# Licensed under the AGPL-v3, see the licence;

from odoo import models, fields, api
from datetime import timedelta

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Projeto',
        default=lambda self: self.get_project_id()
    )
    
    def get_project_id(self):
        project_id = self.env['project.project'].search([
            ('crm_lead_id', '=', self.id)
        ], limit=1, order='id desc')
        if project_id:
            return project_id
        return False
        
    def generate_project(self):    
        if self.stage_id.privacy_visibility == 'followers':
            privacy_visibility = 'followers'
        elif self.stage_id.privacy_visibility == 'employee':
            privacy_visibility = 'employee'
        else:
            privacy_visibility = 'portal'
        
        name = self.partner_id.name if not self.partner_id.parent_id else self.partner_id.parent_id.name
        vals = {
            'name': name,
            'partner_id': self.partner_id.id,
            'user_id': self.env.user.id,
            'privacy_visibility': privacy_visibility,
            'allow_milestones': self.stage_id.allow_milestone,
            'description': self.description
        }
        return self.env['project.project'].create(vals)
    
    def generate_tasks(self, project_id=False):
        template_task_ids = self.env['project.task.template'].search([
            ('active','=',True)
        ]).sorted("sequence")
        for template_task_id in template_task_ids:
            vals = {
                'name': template_task_id.name,
                'project_id': project_id.id,
                'user_ids': [(4, self.env.user.id)],
                'date_deadline': fields.Datetime.now() + timedelta(days=7),
                'partner_id': self.partner_id.id,
            }
            task_id = self.env['project.task'].create(vals)
            if task_id:
                template_task_id.write({'related_project_ids': [(4,project_id.id)]})
    
    def write(self, vals):
        for record in self:
            result = super(CrmLead, record).write(vals)
            if vals.get('stage_id', False):
                stage_id = vals.get('stage_id', False)
                won_stage_id = self.env['crm.stage'].browse(stage_id)
                if won_stage_id.is_won and not record.project_id:
                    project_id = record.generate_project()
                    if project_id:
                        if won_stage_id.auto_generate_basic_tasks:
                            record.generate_tasks(project_id)
                        if not record.project_id:
                            record.write({'project_id': project_id.id})
                        if not project_id.crm_lead_id:
                            project_id.write({'crm_lead_id': record.id})
            return result
    
    def generate_crm_partner(self):
        for record in self:
            company_id = record.env['res.partner']
            partner_id = record.env['res.partner']
            
            if record.partner_name:
                company_id = record.env['res.partner'].create(
                    record.prepare_partner_vals('company')
                )
            
            if not record.partner_id:
                partner_id = record.env['res.partner'].create(
                    record.prepare_partner_vals('person', company_id)
                )
                record.partner_id = partner_id
            
            if company_id and partner_id:
                partner_id.parent_id = company_id
    
    def prepare_partner_vals(self, type='person', company_id=False):
        vals = {
            'name': self.contact_name if type == 'person' else self.partner_name,
            'email': self.email_from,
            'phone': self.phone,
            'mobile': self.mobile or '',
            'street': self.street or '',
            'street2': self.street2 or '',
            'city': self.city or '',
            'state_id': self.state_id.id or False,
            'country_id': self.country_id.id or False,
            'zip': self.zip or '',
            'type': 'contact',
            'is_company': False if type == 'person' else True,
            'parent_id': company_id.id if company_id else False,
        }
        return vals