from odoo import models, fields

class PropertyTag(models.Model):
    _name = "real_estate_tag"
    _description = "Etiquetas de la propiedad"
    
    name = fields.Char(required=True)