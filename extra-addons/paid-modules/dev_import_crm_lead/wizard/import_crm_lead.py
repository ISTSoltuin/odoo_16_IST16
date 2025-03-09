# -*- coding: utf-8 -*-
##############################################################################
#
#    DevIntelle Solution(Odoo Expert)
#    Copyright (C) 2015 Devintelle Soluation (<http://devintellecs.com/>)
#
##############################################################################


from odoo import api, fields, models, _
import datetime
import base64
import csv
from odoo.tools.translate import _
import time
from odoo.exceptions import ValidationError


class import_lead(models.TransientModel):
    _name = "import.lead"

    import_csv = fields.Binary('Import CSV',filters='*.csv')
    
    def get_country(self,name):
        country_id=self.env['res.country'].search([('name','=',name)],limit=1)
        if country_id:
            return country_id.id
        else:
            return False  
    
            
    def get_state(self,name):
        state_id = self.env['res.country.state'].search([('name','=',name)],limit=1)
        if state_id:
            return state_id.id
        else:
            return False 
            
    
    def get_vals(self,csv_line):
        vals={
            'name':csv_line[0],
            'contact_name':csv_line[1],
            'email_from':csv_line[2],
            'phone':csv_line[3],
#            'fax':csv_line[4],
            'state_id':self.get_state(csv_line[5]),
            'country_id':self.get_country(csv_line[6]),
            }
        return vals
        
    def update_product_data(self,product,csv_line):
        vals=self.get_vals(csv_line)
        product.write(vals)
        return True
    
    def create_lead(self,csv_line):
        vals=self.get_vals(csv_line)
        data = self.env['crm.lead'].create(vals)
        return True
    
    def import_lead(self):
        if not self.import_csv:
            raise ValidationError(_('Please Import CSV !'))
        fdata = base64.b64decode(self.import_csv) or False 
        s_data = str(fdata.decode("utf-8"))
        s_data = s_data.split('\n')
        data = []
        for d in s_data:
            if d:
                data.append(d.split(','))
        cnt=0
        for csv_line in data:
            cnt+=1
            if cnt == 1:
                continue
            if len(csv_line) == 1:
                line = csv_line[0].split(';')
                csv_line=[]
                for l in line:
                    csv_line.append(l)
            else:
                self.create_lead(csv_line)
        return True
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
