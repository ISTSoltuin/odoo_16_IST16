# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"


class RenLead(models.Model):
    """REN Lead"""
    _name = 'ren.lead'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = __doc__
    _rec_name = 'title'

    title = fields.Char(string="Title", required=True)
    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")

    customer_street = fields.Char(string="Street", translate=True)
    customer_street2 = fields.Char(string="Street 2", translate=True)
    customer_city = fields.Char(string="City", translate=True)
    customer_state_id = fields.Many2one("res.country.state", string="State")
    customer_zip = fields.Char(string="Zip", size=6)
    customer_country_id = fields.Many2one("res.country", string="Country")

    customer_category = fields.Selection(
        [('residential', "Residential"), ('institutional', "Institutional"), ('industrial', "Industrial"),
         ('commerical', "Commerical"), ('government', "Government"), ('social_sector', "Social Sector")],
        string="Customer Category", default='residential')

    site_street = fields.Char(translate=True)
    site_street2 = fields.Char(translate=True)
    site_city = fields.Char(translate=True)
    site_state_id = fields.Many2one("res.country.state")
    site_country_id = fields.Many2one("res.country")
    site_zip = fields.Char(size=6)
    site_latitude_location = fields.Char(string='Latitude')
    site_longitude_location = fields.Char(string='Longitude')

    existing_connection = fields.Char(string="Existing Connection")
    monthly_electric_bill = fields.Monetary(string="Monthly Electric Bill")
    consumer_no = fields.Char(string="Consumer No")
    existing_supply_volt = fields.Char(string="Existing Supply Volts")

    site_usage = fields.Char(string="Site Usage")
    type_of_property = fields.Selection([('semi', "Semi"), ('terraced', "Terraced"), ('detached', "Detached")],
                                        string="Type of Property")
    age_of_property = fields.Char(string="Age of Property")

    service_type = fields.Selection([('power_backup', "Power Backup"), ('solar_water_heater', "Solar Water Heater"),
                                     ('solar_water_pump', "Solar Water Pump"), ('offgrid_solar', "Offgrid Solar"),
                                     ('solar_street_light', "Solar Street Light"),
                                     ('containerised Solar', "Containerised Solar")], string="Service Type")
    contract_demand = fields.Char(string="Contract Demand")
    estimate_quotation = fields.Monetary(string="Estimate Quotation")

    responsible = fields.Many2one('res.users', default=lambda self: self.env.user, required=True)
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="Priority",
                                default='0')
    partner_id = fields.Many2one("res.partner", string="Customer", ondelete="cascade", readonly=True)

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', related="company_id.currency_id")

    renewable_energy_order_id = fields.Many2one('renewable.energy.order', string="REN Order")

    lead_source_type = fields.Selection(
        [('phone_calls', "Phone Calls"), ('e_mail', "E-Mail"), ('social_media', "Social Media"), ('website', "Website"),
         ('direct_mail', "Direct Mail"), ('events', "Events"), ('public_relations', "Public Relations"),
         ('content_marketing', "Content Marketing"), ('branding', "Branding"), ('online_marketing', "Online Marketing"),
         ('referrals', "Referrals")], string="Lead Source Type")
    source_type_description = fields.Char(string="Description")

    status = fields.Selection(
        [('a_new', "New"), ('b_in_discussion', "In Discussion"), ('c_won', "Won"), ('d_lost', "Lost")],
        string="Status", default='a_new')
    feedback = fields.Html(string="Feedback")


    def a_new_to_b_in_discussion(self):
        self.status = 'b_in_discussion'

    def b_in_discussion_to_c_won(self):
        self.status = 'c_won'

    def c_won_to_d_lost(self):
        self.status = 'd_lost'

    def get_create_customer(self):
        data = {
            "name": self.name,
            "street": self.customer_street,
            "street2": self.customer_street2,
            "city": self.customer_city,
            "state_id": self.customer_state_id.id,
            "zip": self.customer_zip,
            "country_id": self.customer_country_id.id,
            "user_id": self.responsible.id,
            "phone": self.phone,
            "email": self.email,
        }
        partner_id = self.env["res.partner"].create(data)
        self.partner_id = partner_id.id

    def get_create_ren_order(self):
        data = {
            'customer_id': self.partner_id.id,
            'phone': self.phone,
            'email': self.email,
            "customer_street": self.customer_street,
            "customer_street2": self.customer_street2,
            "customer_city": self.customer_city,
            "customer_state_id": self.customer_state_id.id,
            "customer_zip": self.customer_zip,
            "customer_country_id": self.customer_country_id.id,
            "priority": self.priority,
            "site_usage": self.site_usage,
            "type_of_property": self.type_of_property,
            "age_of_property": self.age_of_property,
            "site_street": self.site_street,
            "site_street2": self.site_street2,
            "site_city": self.site_city,
            "site_state_id": self.site_state_id.id,
            "site_country_id": self.site_country_id.id,
            "site_zip": self.site_zip,
            "site_latitude_location": self.site_latitude_location,
            "site_longitude_location": self.site_longitude_location,
            "service_type": self.service_type,
            "contract_demand": self.contract_demand,
            "estimate_quotation": self.estimate_quotation,
        }
        renewable_energy_order_id = self.env['renewable.energy.order'].create(data)
        self.renewable_energy_order_id = renewable_energy_order_id.id
