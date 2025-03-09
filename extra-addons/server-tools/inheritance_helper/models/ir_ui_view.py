from odoo import fields, models, api
from odoo.tools import apply_inheritance_specs
import logging
_logger = logging.getLogger()

class View(models.Model):
    _inherit = 'ir.ui.view'
    
    def apply_inheritance_specs(self, source, specs_tree, pre_locate=lambda s: True):
        try:
            source = apply_inheritance_specs(
                source, specs_tree,
                inherit_branding=self._context.get('inherit_branding'),
                pre_locate=pre_locate,
            )
        except ValueError as e:
            # TODO: 
            # 1. Sanitizar View filha sem modulo e external id não exibido no front-end
            #   1.1 Sanitização deve ocorrer numa nova recursão da subrotina do apply_inheritance_specs
            #   1.2 Fluxo: se view não tem módulo, é garbage, implementar garbage collector (unlink da view)
            
            _logger.info(e)
        return source