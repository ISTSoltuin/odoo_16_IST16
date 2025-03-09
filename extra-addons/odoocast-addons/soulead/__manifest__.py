{
    'name': 'Soulead',
    'version': '1.0',
    'category': 'Social',
    'summary': 'Schedule posts on Facebook and Instagram',
    'author': 'Your Name',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/social_media_account_views.xml',
        'views/social_media_post_views.xml',
        'views/social_media_dashboard_views.xml',
        # 'views/templates.xml',
    ],
    'installable': True,
    'application': True,
}
