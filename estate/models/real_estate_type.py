from odoo import models, fields

class RealEstateType(models.Model):
    _name = "real_estate_type"
    _description = "Tipos de casas"
    
    name = fields.Char(required=True, string="Name")
    
    
    