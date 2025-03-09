# -*- coding: utf-8 -*-
# Copyright (C) 2023-TODAY TechKhedut (<https://www.techkhedut.com>)
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
import uuid
from odoo import fields, models, api


class PropertyRentalConfig(models.Model):
    _inherit = 'property.details'

    # website listing features
    web_gym = fields.Boolean('Gym')
    web_wifi = fields.Boolean('WiFi')
    web_parking = fields.Boolean('Parking')
    web_pool = fields.Boolean('Pool')
    web_security = fields.Boolean('Security')
    web_laundry = fields.Boolean('Laundry Room')
    web_equip_kitchen = fields.Boolean('Equipped Kitchen')
    web_air_condition = fields.Boolean('Air Conditioned')
    web_semi_furnish = fields.Boolean('Semi Furnished')
    web_full_furnish = fields.Boolean('Full Furnished')
    web_alarm = fields.Boolean('Safety Alarm')
    web_window_cover = fields.Boolean('Window Covering')
    accommodation = fields.Integer('Accommodation')

    similar_properties = fields.Many2many('property.details', 'similar_property_rel', 'sp_id', 'property_id',
                                          string="Similar Properties")

    website_description = fields.Html(string="Website Description")
    short_description = fields.Char(string="Short Description", size=150)

    access_token = fields.Char()
    is_popular_list = fields.Boolean(string="Is Popular Listing ?")
    is_verify = fields.Boolean(string="Is Verified ?")

    lead_count = fields.Integer(string="Leads", compute='_get_lead_count')

    def _get_lead_count(self):
        for rec in self:
            leads = 0
            if rec.id:
                leads = self.env['crm.lead'].sudo().search_count([('property_id', '=', rec.id)])
            rec.lead_count = leads

    def assign_access_token(self):
        self.access_token = str(uuid.uuid4())

    def action_get_leads(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Property Leads',
            'res_model': 'crm.lead',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
            'view_mode': 'tree,form',
            'target': 'current'
        }

    @api.model
    def create(self, vals):
        vals['access_token'] = str(uuid.uuid4())
        return super(PropertyRentalConfig, self).create(vals)

    def get_all_cities(self):
        cities = self.env['property.details'].sudo().search([('stage', '=', 'available')]).mapped('city_id')
        city_list = []
        if cities:
            city_list = sorted(cities.mapped('name'))
        return city_list


class PropertyBookmark(models.Model):
    """Property Bookmark"""
    _name = 'property.bookmark'
    _description = __doc__

    partner_id = fields.Many2one('res.partner', string="User")
    property_id = fields.Many2one('property.details', string="Property")
