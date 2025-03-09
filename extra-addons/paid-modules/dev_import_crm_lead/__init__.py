# -*- coding: utf-8 -*-
##############################################################################
#
#    DevIntelle Solution(Odoo Expert)
#    Copyright (C) 2015 Devintelle Soluation (<http://devintellecs.com/>)
#
##############################################################################

from . import wizard

def pre_init_check(cr):
    from odoo.service import common
    from odoo import api, fields, models, SUPERUSER_ID, _
    from odoo.exceptions import AccessError, UserError, ValidationError
    version_info = common.exp_version()
    server_serie = version_info.get('server_serie')
    if server_serie != '16.0':
        raise UserError(
                    'Module support Odoo Vrsion 16.0 found {}.'.format(server_serie))
    return True
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
