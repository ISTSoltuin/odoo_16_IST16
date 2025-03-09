# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################


{
    'name': 'Import CRM Lead by CSV/XLS',
    'version': '16.0.1.0',
    'sequence': 1,
    'category': 'Sales',
    'description':
        """
 Apps will help to Import CRM Lead by CSV or XLS format
        
        import Lead , import CRM Lead, import CRM Lead by csv, import CRM Lead by xls, import CRM Lead ,
		CRM Lead, CRM Lead Csv, CRM Lead by XSL
Import CRM Lead by CSV/XLS

Odoo Import CRM Lead by CSV/XLS

Import CRM

Odoo import CRM

Import CRM leads

Odoo import CRM leads

Import CRM leads by CSV

Odoo Import CRM leads by CSV

Import CRM leads by XLS

Odoo Import CRM leads by XLS

Import CRM leads by excel

Odoo Import CRM leads by excel

Import CRM Leads through CSV/XLS 

Odoo Import CRM Leads through CSV/XLS 

Import CRM leads through csv

Odoo import CRM leads through csv

Import CRm leads through XLS

Odoo import CRM leads through XLS

Import CRm leads through excel

Odoo import CRM leads through excel

Apps will help to Import CRM Leads in CSV or XLS format

Odoo Apps will help to Import CRM Leads in CSV or XLS format

CRM Leads

Odoo CRM Leads

Manage CRM Leads

Odoo Manage CRM Leads

Apps will help to Import CRM Leads in CSV or XLS format

Odoo Apps will help to Import CRM Leads in CSV or XLS format

Install xlrd Python Package before installing a module

Odoo Install xlrd Python Package before installing a module

Import Lead Menu

Odoo Import Lead Menu

Manage Import Lead Menu

Odoo Manage Import Lead Menu

Import leads

Odoo Import Leads

Manage Import Leads

Odoo Manage Import Leads

Odoo Management

Odoo developer

Odoo

Odoo Apps

CRM Leads into CSV

Odoo CRM Leads into CSV

Manage CRM Leads into CSV

Odoo Manage CRM Leads into CSV

CRM Leads into Excel

Odoo CRM leads into Excel

Manage CRM Leads into Excel

Odoo Manage CRM Leads into Excel

CRM Leads into XLS

Odoo CRM leads into XLS

Manage CRM Leads into XLS

Odoo Manage CRM Leads into XLS

CRM Leads through XLS

Odoo CRM leads through XLS

Manage CRM Leads through XLS

Odoo Manage CRM Leads through XLS

CRM Leads through CSV

Odoo CRM leads through CSV

Manage CRM Leads through CSV

Odoo Manage CRM Leads through CSV

CRM Leads through Excel

Odoo CRM leads through Excel

Manage CRM Leads through Excel

Odoo Manage CRM Leads through Excel

    """,
    'summary': 'Apps will help to Import CRM Lead by CSV or XLS format',
    'author': 'Devintelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_crm_lead.xml',
        ],
    'demo': [],
    'test': [],
    'css': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price':15.0,
    'currency':'EUR',
    'pre_init_hook' :'pre_init_check',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
