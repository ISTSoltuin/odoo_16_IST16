# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Advanced Activity Dashboard',
    'version': '16.0.1.0.0',
    'live_test_url': 'https://youtu.be/FBHFxKGsA5E',
    'sequence': 1,
    'summary': """
        All in one advanced dashboard for users to preview its activities, Mail activity, All in one Odoo dashboard, 
        All in one Dashboard Activity, All in one Activity Dashboard, Web Responsive dashboard, Activity Management, 
        Activities Dashboard, Dashboard Activities, Tableau de bord des activités, Dashboard Odoo Activity, Graphs,
        Activity Odoo Dashboard, Web Dashboard, All in one Activities, Planned Activities, All in one Activity,
        History Activity monitoring Activity, Mail Activity Board, Schedule activities Scheduler, Planned Activity,
        Advanced List Activities, Multi Company Activity, Mail Odoo Print,, Daily Activities Management, Télécharger,
        Advance Dashboard, All ine one dynamic dashboard, Dynamic Activity Dashboards, Custom Odoo Dashboard, Exporter,
        Odoo Charts, Dashboard Charts, Activity Scheduler Users, Activity Supervisor, Activity Search Filter, Imprimer,
        Activity Search Filter, Activity Multi Activity Schedule, Schedule Mass Activity, Tag activity history, KPI, 
        Dashboard Features, Schedule Activity Management, Advance List Activity, Mail Activity List, Daily Activity,
        Print Activities, Print Activity, Export Activities, Export Activity, Download Activities, Download Activity,
        Print Dashboard, Print Dashboard, Export Dashboard, Export Dashboard, Download Dashboard, Download Dashboard,
        Supervise Activity, Supervise Dasboard, Advance List View Manager, Dynamic Filters Search, Dynamic Search, 
        Dashboard Apps, Key Performance Indicators, Dashboard View, DashboardView, Advanced List View Manager, 
        Advanced ListView Manager, Advance ListView Manager, Dynamic List View, Advanced GraphView, Supervise Activities, 
        Dynamic ListView, Automated Dashboard, Dashboard Automation, Dashboard Customization, Multi Task Activity,
        Multi Task Dashboard, Multi Dashboard Task, Activity Tasks Dashboard, Analytic Data Dashboard Analytic,
        KPI Dashboard Powerful Dashboard KPI, Beautiful Dashboard, Elegant Dashboard, Users Dashboard, User Dashboard,
        Dashboard Users, Dashboard per users, Dashboard Widget Templates, Today Report Dashboard Reports, Dashboard Tile,
        Portal Dashboard, Web Dynamic Dashboard Dynamic Web Backend Activities Dashboards, Manage All Activities,
        Advance Graph View, Advanced Graph View, CRM Dashboard CRM, Odoo Advance Activity Management, Advance GraphView
        Customer Dashboard Customers, Employee Dashboard Employees, Sale Dashboard Sale, Purchase Dashboard Purchases, 
        Sales Dashboard Sales, Invoice Dashboard Invoice, Account Dashboard Accounts, Project Dashboard Projects,
        Lead Dashboard Leads, Opportunity Dashboard Opportunity, Opportunities Dashboard Opportunities, Leads Dashboard,
        Activity Monitoring, Activity Views, Schedule Activity, Manage Activities, New design, Web Backend dashboard            
    """,
    'description': "An amazing dashboard for users to preview its activities with highly useful filters and features.",
    'author': 'Innoway',
    'maintainer': 'Innoway',
    'price': '15.0',
    'currency': 'EUR',
    'website': 'https://innoway-solutions.com',
    'license': 'OPL-1',
    'images': [
        'static/description/wallpaper.png'
    ],
    'depends': [
        'web',
        'mail'
    ],
    'data': [
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'activity_dashboard/static/lib/jquery.dataTables.min.js',
            'activity_dashboard/static/lib/dataTables.bootstrap5.min.js',
            'activity_dashboard/static/lib/dataTables.buttons.min.js',
            'activity_dashboard/static/lib/jszip.min.js',
            'activity_dashboard/static/lib/pdfmake.min.js',
            'activity_dashboard/static/lib/vfs_fonts.js',
            'activity_dashboard/static/lib/buttons.html5.min.js',
            'activity_dashboard/static/src/xml/activity_dashboard.xml',
            'activity_dashboard/static/src/scss/activity_dashboard.scss',
            'activity_dashboard/static/src/js/activity_dashboard.js',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
