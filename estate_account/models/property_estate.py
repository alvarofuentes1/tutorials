from odoo import models

class PropertyEstate(models.Model):
    _inherit = "real_estate"
    
    def action_set_sold(self):
        print(" Método action_set_sold sobrescrito desde estate_account")
        
        return super().action_set_sold()