# -*- coding: utf-8 -*-

from odoo import models
from odoo.addons.web.models import ir_http

class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        connect_parameter_id = self.env.ref('web_enterprise_extended.can_connect_external_odoo_api')
        can_connect_external_odoo_api = False
        if connect_parameter_id:
            if connect_parameter_id.value == 'True':
                can_connect_external_odoo_api = True
            if can_connect_external_odoo_api:
                return super(Http, self).session_info()
            else:
                return self.custom_session_info()
    
    def custom_session_info(self):
        result = ir_http.Http.session_info(self)
        return result