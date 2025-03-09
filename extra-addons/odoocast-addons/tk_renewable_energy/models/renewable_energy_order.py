# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api
from datetime import date


class SaleOrder(models.Model):
    _inherit = 'sale.order'


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    renewable_energy_order_id = fields.Many2one('renewable.energy.order', string='REN Order')


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    renewable_energy_order_id = fields.Many2one('renewable.energy.order', string='REN Order')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    team_type = fields.Selection(
        [('survey_team', "Survey Team"), ('installation_team', "Installation Team"), ('qa_team', "QA Team")],
        string="Team Type")


class RenewableEnergyOrder(models.Model):
    """Renewable Energy Order"""
    _name = 'renewable.energy.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = __doc__
    _rec_name = 'order_number'

    order_number = fields.Char(string='REN No', required=True, readonly=True, default=lambda self: ('New'))
    date_of_order = fields.Date(string="Date of Order")
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    phone = fields.Char(related="customer_id.phone", string="Phone")
    email = fields.Char(related="customer_id.email", string="Email")
    responsible = fields.Many2one('res.users', default=lambda self: self.env.user, required=True)
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="Priority",
                                default='0')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    customer_street = fields.Char(string="Street", translate=True)
    customer_street2 = fields.Char(string="Street 2", translate=True)
    customer_city = fields.Char(string="City", translate=True)
    customer_state_id = fields.Many2one("res.country.state", string="State")
    customer_zip = fields.Char(string="Zip", size=6)
    customer_country_id = fields.Many2one("res.country", string="Country")

    site_street = fields.Char(translate=True)
    site_street2 = fields.Char(translate=True)
    site_city = fields.Char(translate=True)
    site_state_id = fields.Many2one("res.country.state")
    site_country_id = fields.Many2one("res.country")
    site_zip = fields.Char(size=6)
    site_latitude_location = fields.Char(string='Latitude ')
    site_longitude_location = fields.Char(string=' Longitude')

    site_usage = fields.Char(string="Site Usage")
    type_of_property = fields.Selection([('semi', "Semi"), ('terraced', "Terraced"), ('detached', "Detached")],
                                        string="Type of Property")
    age_of_property = fields.Char(string="Age of Property")

    contract_demand = fields.Char(string="Contract Demand")
    service_type = fields.Selection([('power_backup', "Power Backup"), ('solar_water_heater', "Solar Water Heater"),
                                     ('solar_water_pump', "Solar Water Pump"), ('offgrid_solar', "Offgrid Solar"),
                                     ('solar_street_light', "Solar Street Light"),
                                     ('containerised Solar', "Containerised Solar")], string="Service Type")

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', related="company_id.currency_id")
    estimate_quotation = fields.Monetary(string="Estimate Quotation")
    description = fields.Html(string="Description")

    ren_quotation_ids = fields.One2many('ren.quotation', 'renewable_energy_order_id', string="Quotation")
    total_quotation = fields.Monetary(string="Total Quotation", compute="_total_quotation", store=True)

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    state = fields.Selection(
        selection=[
            ('draft', "Quotation"),
            ('sent', "Quotation Sent"),
            ('sale', "Sales Order"),
            ('done', "Locked"),
            ('cancel', "Cancelled"),
        ],
        default='draft',
        string='State',
        compute='compute_renewable_energy_order'
    )

    bill_of_material_order_id = fields.Many2one('mrp.bom', string='Bill of Material')
    manufacturing_order_id = fields.Many2one('mrp.production', string='Manufacturing Order')
    manufacturing_state = fields.Selection(related="manufacturing_order_id.state")

    order_stages = fields.Selection(
        [('new', "New"), ('site_inspection', "Site Inspection"), ('material_order', "Material Order"),
         ('material_arrived', "Material Arrived"), ('project_installation', "Project Installation"),
         ('qa_check', "QA Check"), ('complete', "Complete"), ('cancel', "Cancel")], string="Order Stages",
        default='new')

    ren_survey_document_ids = fields.One2many('ren.survey.document', 'renewable_energy_order_id',
                                              string="Survey Document")
    site_survey_image_ids = fields.One2many('site.survey.image', 'renewable_energy_order_id',
                                            string="Site Survey Image")

    survey_team_id = fields.Many2one('survey.team', string="Survey Team")
    survey_member_id = fields.Many2one('res.users', string="Survey Member")
    survey_project_id = fields.Many2one(related='survey_team_id.survey_project_id')
    survey_task_id = fields.Many2one('project.task', readonly=True, store=True)
    survey_task_count = fields.Integer(compute='_compute_survey_task_count')

    qa_team_id = fields.Many2one('qa.team', string="Team ")
    qa_member_id = fields.Many2one('res.users', string="Member")
    qa_team_project_id = fields.Many2one(related="qa_team_id.qa_team_project_id")
    qa_task_count = fields.Integer(compute='_compute_qa_task_count')
    qa_task_id = fields.Many2one('project.task', readonly=True, store=True)

    installation_team_id = fields.Many2one('installation.team', string=" Team")
    installation_member_ids = fields.Many2many('res.users', string="Members")
    installation_team_project_id = fields.Many2one(related="installation_team_id.project_installation_team_id")
    installation_task_id = fields.Many2one('project.task', readonly=True, store=True)
    installation_task_count = fields.Integer(compute="_compute_installation_task_count")

    date_of_inspection = fields.Date(string="Date of Inspection")
    site_remarks = fields.Text(string="Site Remarks")

    ren_bom_ids = fields.One2many('ren.bom', 'renewable_energy_order_id', string="Material of Project")

    start_date = fields.Date(string='Start Date', default=fields.date.today(), required=True)
    end_date = fields.Date(string='End Date', default=fields.date.today(), required=True)
    hours = fields.Integer(compute='day_compute_hours', string='Hours')
    days = fields.Integer(compute='day_compute_hours', string='Days')

    qa_status = fields.Selection([('pass', "Pass"), ('need_to_review', "Need to Review")], string="QA Status")
    remarks = fields.Html(string="Remarks")

    warranty_template_id = fields.Many2one('warranty.template', string="Warranty Template")
    warranty_covered = fields.Html(string="Warranty Covered")
    warranty_not_covered = fields.Html(string="Warranty Not Covered")

    @api.onchange('warranty_template_id')
    def get_warranty_template(self):
        for rec in self:
            if rec.warranty_template_id:
                rec.warranty_covered = rec.warranty_template_id.warranty_covered
                rec.warranty_not_covered = rec.warranty_template_id.warranty_not_covered

    def action_qa_pass(self):
        self.qa_status = 'pass'

    def action_review(self):
        self.qa_status = 'need_to_review'

    @api.depends('end_date', 'start_date')
    def day_compute_hours(self):
        for rec in self:
            installation_end_date = fields.Datetime.to_datetime(rec.end_date)
            installation_start_date = fields.Datetime.to_datetime(rec.start_date)
            daysLeft = installation_end_date - installation_start_date

            years = ((daysLeft.total_seconds()) / (365.242 * 24 * 3600))
            yearsInt = int(years)

            months = (years - yearsInt) * 12
            monthsInt = int(months)

            days = (months - monthsInt) * (365.242 / 12)
            daysInt = int(days)
            rec.days = daysInt

            hours = (days - daysInt) * 24
            hoursInt = int(hours)

            minutes = (hours - hoursInt) * 60
            minutesInt = int(minutes)

            seconds = (minutes - minutesInt) * 60
            secondsInt = int(seconds)

            if days <= 0:
                rec.hours = 0
            else:
                days_hour = daysInt * 24
                rec.hours = hoursInt + days_hour

    @api.onchange('survey_team_id', 'survey_member_id')
    def get_team_member(self):
        for rec in self:
            members = []
            if rec.survey_team_id:
                for data in rec.survey_team_id.employee_ids:
                    members.append(data.id)
                return {'domain': {'survey_member_id': [('id', 'in', members)]}}

    @api.onchange('installation_team_id', 'installation_member_ids')
    def get_installation_team_member(self):
        for rec in self:
            installation_members = []
            if rec.installation_team_id:
                for data in rec.installation_team_id.employee_ids:
                    installation_members.append(data.id)
                return {'domain': {'installation_member_ids': [('id', 'in', installation_members)]}}

    @api.onchange('qa_team_id', 'qa_member_id')
    def getqa_team_member(self):
        for rec in self:
            qa_members = []
            if rec.qa_team_id:
                for data in rec.qa_team_id.employee_ids:
                    qa_members.append(data.id)
                return {'domain': {'qa_member_id': [('id', 'in', qa_members)]}}

    def new_to_site_inspection(self):
        self.order_stages = 'site_inspection'

    def site_inspection_to_material_order(self):
        self.order_stages = 'material_order'

    def material_order_to_material_arrived(self):
        self.order_stages = 'material_arrived'

    def material_arrived_to_project_installation(self):
        self.order_stages = 'project_installation'

    def project_installation_to_qa_check(self):
        self.order_stages = 'qa_check'

    def qa_check_to_complete(self):
        self.order_stages = 'complete'

    def complete_to_cancel(self):
        self.order_stages = 'cancel'

    @api.model
    def create(self, vals):
        if vals.get('order_number', ('New')) == ('New'):
            vals['order_number'] = self.env['ir.sequence'].next_by_code(
                'renewable.energy.order') or ('New')
        res = super(RenewableEnergyOrder, self).create(vals)
        return res

    @api.depends('ren_quotation_ids')
    def _total_quotation(self):
        for rec in self:
            total_quotation = 0.0
            if rec.ren_quotation_ids:
                for quot in rec.ren_quotation_ids:
                    total_quotation = total_quotation + quot.price
                    rec.total_quotation = total_quotation
            else:
                rec.total_quotation = 0.0

    def action_create_quotation(self):
        order_line = []
        for record in self.ren_quotation_ids:
            solar_product_record = {
                'product_id': self.env.ref('tk_renewable_energy.solar_product').id,
                'name': record.description,
                'price_unit': record.price,
            }
            order_line.append((0, 0, solar_product_record)),
        data = {
            'partner_id': self.customer_id.id,
            'date_order': fields.Datetime.now(),
            'order_line': order_line,
        }
        sale_order_id = self.env['sale.order'].sudo().create(data)
        self.sale_order_id = sale_order_id.id

    def action_create_bill_of_material(self):
        bill_of_material_order_line = []
        for record in self.ren_bom_ids:
            bill_of_material_product_record = {
                'product_id': record.product_id.id,
                'product_qty': record.product_qty,
            }
            bill_of_material_order_line.append((0, 0, bill_of_material_product_record)),
        for rec in self.ren_quotation_ids:
            data = {
                'product_tmpl_id': rec.product_id.product_tmpl_id.id,
                'product_qty': 1,
                'code': self.order_number,
                'bom_line_ids': bill_of_material_order_line,
                'renewable_energy_order_id': self.id
            }
            bill_of_material_order_id = self.env['mrp.bom'].sudo().create(data)
            self.bill_of_material_order_id = bill_of_material_order_id.id

    def action_create_manufacturing_order(self):
        manufacturing_order_line = []
        for record in self.ren_bom_ids:
            manufacturing_product_record = {
                'product_id': record.product_id.id,
                'product_uom_qty': record.product_qty,
                'product_uom': record.product_id.uom_id.id,
            }
            manufacturing_order_line.append((0, 0, manufacturing_product_record)),

        for record in self.ren_quotation_ids:
            data = {
                'product_id': record.product_id.id,
                'product_qty': 1,
                'product_uom_id': record.product_id.uom_id.id,
                'bom_id': self.bill_of_material_order_id.id,
                'renewable_energy_order_id': self.id
            }
        manufacturing_order_id = self.env['mrp.production'].sudo().create(data)
        moves_raw_values = manufacturing_order_id._get_moves_raw_values()
        list_move_raw = []
        for move_raw_values in moves_raw_values:
            list_move_raw += [(0, 0, move_raw_values)]

        manufacturing_order_id.write({'move_raw_ids': list_move_raw})
        self.manufacturing_order_id = manufacturing_order_id.id

    def create_survey_task(self):
        task_id = self.env['project.task'].sudo().create({
            'name': self.survey_project_id.name,
            'project_id': self.survey_project_id.id,
            'user_ids': self.survey_member_id.ids,
            'date_assign': self.date_of_inspection,
            'team_type': 'survey_team'
        })
        self.survey_task_id = task_id.id

    def create_QA_task(self):
        task_id = self.env['project.task'].sudo().create({
            'name': self.qa_team_project_id.name,
            'project_id': self.qa_team_project_id.id,
            'user_ids': self.qa_member_id.ids,
            'date_assign': self.date_of_inspection,
            'team_type': 'qa_team'
        })
        self.qa_task_id = task_id.id

    def create_installation_task(self):
        installation_id = self.env['project.task'].sudo().create({
            'name': self.installation_team_project_id.name,
            'project_id': self.installation_team_project_id.id,
            'user_ids': self.installation_member_ids.ids,
            'date_assign': self.start_date,
            'date_last_stage_update': self.end_date,
            'team_type': 'installation_team'
        })
        self.installation_task_id = installation_id.id

    def _compute_qa_task_count(self):
        for rec in self:
            qa_task_count = self.env['project.task'].search_count([('project_id', '=', self.qa_team_project_id.id)])
            rec.qa_task_count = qa_task_count
        return True

    def action_qa_task(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'QA Tasks',
            'res_model': 'project.task',
            'domain': [('project_id', '=', self.qa_team_project_id.id)],
            'view_mode': 'tree,form',
            'terget': 'current',
        }

    def _compute_survey_task_count(self):
        for rec in self:
            survey_task_count = self.env['project.task'].search_count([('project_id', '=', self.survey_project_id.id)])
            rec.survey_task_count = survey_task_count
        return True

    def action_survey_task(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Survey Tasks',
            'res_model': 'project.task',
            'domain': [('project_id', '=', self.survey_project_id.id)],
            'view_mode': 'tree,form',
            'terget': 'current',
        }

    def _compute_installation_task_count(self):
        for rec in self:
            installation_task_count = self.env['project.task'].search_count(
                [('project_id', '=', self.installation_team_project_id.id)])
            rec.installation_task_count = installation_task_count
        return True

    def action_installation_task(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Installation Tasks',
            'res_model': 'project.task',
            'domain': [('project_id', '=', self.installation_team_project_id.id)],
            'view_mode': 'tree,form',
            'terget': 'current',
        }

    @api.depends('sale_order_id.state')
    def compute_renewable_energy_order(self):
        for record in self:
            if record.sale_order_id:
                if record.state != record.sale_order_id.state:
                    record.state = record.sale_order_id.state