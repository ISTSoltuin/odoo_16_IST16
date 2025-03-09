# -*- coding: utf-8 -*-

from odoo import api, models, fields
import logging
_logger = logging.getLogger(__name__)

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    state = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned')], 'State',
        compute='_compute_state', store=True)

class DashboardActivity(models.Model):
    _name = 'dashboard.activity'

    @api.model
    def get_activities(self):

        

        all_activities = self.env['mail.activity'].search([('user_id', '=', self.env.user.id)])

        overdue_activities = self.env['mail.activity'].search([('state', '=', 'overdue'),('user_id', '=', self.env.user.id)])
        today_activities = self.env['mail.activity'].search([('state', '=', 'today'),('user_id', '=', self.env.user.id)])
        planned_activities = self.env['mail.activity'].search([('state', '=', 'planned'),('user_id', '=', self.env.user.id)])

        activities = [len(all_activities), len(planned_activities), len(today_activities), len(overdue_activities)]

        list_planned_activity = []
        for item in planned_activities:
            activity = [item.summary, item.activity_type_id.name, item.date_deadline, item.state.capitalize(), item.id]
            list_planned_activity.append(activity)

        list_today_activity = []
        for item in today_activities:
            activity = [item.summary, item.activity_type_id.name, item.date_deadline, item.state.capitalize(), item.id]
            list_today_activity.append(activity)

        list_overdue_activity = []
        for item in overdue_activities:
            activity = [item.summary, item.activity_type_id.name, item.date_deadline, item.state.capitalize(), item.id]
            list_overdue_activity.append(activity)
        
        return {
            'activities' : activities,
            'list_planned_activity' : list_planned_activity,
            'list_today_activity' : list_today_activity,
            'list_overdue_activity' : list_overdue_activity,
        }