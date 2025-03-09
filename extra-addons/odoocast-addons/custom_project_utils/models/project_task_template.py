# Copyright @ODOOCAST 2024 contato@odoocast.com.br
# Licensed under the AGPL-v3, see the licence;

from odoo import models, fields, api
from odoo.exceptions import UserError

class ProjectTaskTemplate(models.Model):
    _name = 'project.task.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Project Task Template'
    _order = 'sequence'
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help="If the active field is set to false, it will allow you to hide the task without removing it."
    )
    
    name = fields.Char(
        string='Name', 
        tracking=True
    )
    
    description = fields.Text(
        string='Description',
        help="Description of the task",
        tracking=True
    )
    
    priority = fields.Selection([
            ('0', 'Low'),
            ('1', 'Normal'),
            ('2', 'High'),
            ('3', 'Very High')
        ], 
        string='Priority', 
        default='1', 
        help="Task priority",
        tracking=True
    )
    
    sequence = fields.Integer(
        string='Sequence',
        help="Gives the sequence order when displaying a list of project task templates."
    )
    
    date_end_interval = fields.Integer(
        string='Days quantity to end date',
        default=0,
        help="Days quantity to end date",
    )
    
    deadline_interval = fields.Integer(
        string='Deadline Interval (daýs)',
        default=0,
        help="Deadline interval in days"
    )
    
    default_planned_hours = fields.Float(
        string='Default Planned Hours',
        default=0,
        help="Default planned hours for the task"
    )
    
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company related to this task"
    )
    
    allow_subtask = fields.Boolean(
        string='Allow Subtask',
        default=False,
        help="Allows the creation of subtasks"
    )
    
    allow_milestone = fields.Boolean(
        string='Allow Milestone',
        default=False,
        help="Allows the creation of milestones"
    )
    
    allow_task_dependencies = fields.Boolean(
        string='Allow Task Dependencies',
        default=False,
        help="Allows the creation of task dependencies"
    )
    
    allow_recurring_task = fields.Boolean(
        string='Allow Recurring Task',
        default=False,
        help="Allows the creation of recurring tasks"
    )
    
    related_project_ids = fields.Many2many(
        comodel_name='project.project',
        relation='project_task_template_project_rel',
        column1='task_template_id',
        column2='project_id',
        string='Related Projects',
        help="Related projects"
    )
    
    state = fields.Selection([
            ('draft', 'Draft'),
            ('confirm', 'Confirmed'),
            ('cancel', 'Cancelled'),
            ('active','Active'),
            ('inactive','Inactive'),
        ],
        string='Status', 
        default='draft', 
        tracking=True, 
        help="The status of the task."
    )
    
    def compute_name(self):
        for record in self:
            record.name = f"[{record.sequence + 1}] Project Task Template"

    def action_confirm(self):
        for record in self:
            record.state = 'confirm'
    
    def action_cancel(self):
        for record in self:
            record.state = 'cancel'
    
    def action_draft(self):
        for record in self:
            record.state = 'draft'
    
    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise UserError("You can't delete a task template in a confirmed state.")
            record.action_archive()
    
    def action_archive(self):
        for record in self:
            super(ProjectTaskTemplate, record).action_archive()
            record.state = 'inactive'
    
    def action_unarchive(self):
        for record in self:
            super(ProjectTaskTemplate, record).action_unarchive()
            record.state = 'active'
