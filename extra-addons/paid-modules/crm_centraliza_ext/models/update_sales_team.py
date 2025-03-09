from odoo import api, SUPERUSER_ID

def update_crm_team_view(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    view_id = env.ref('sales_team.crm_team_view_tree')
    if view_id:
        view_id.write({'arch': view_id.arch.replace("Sales Team", "Pipelines")})