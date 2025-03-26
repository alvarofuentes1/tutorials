from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RealEstateType(models.Model):
    _name = "real_estate_type"
    _description = "Tipos de casas"
    _order = "name"

    
    name = fields.Char(required=True, string="Name")
    property_ids = fields.One2many("real_estate", "property_type", string="Properties")
    sequence = fields.Integer(default=10)
    
    @api.constrains("name")
    def _check_unique_name(self):
        for type in self:
            existing_types = self.search([
                ("id", "!=", type.id),
                ("name", "ilike", type.name) #ilike realiza una busqueda sin tener en cuenta minusculas y mayusculas
            ])
            if existing_types:
                raise ValidationError("The property type name must be unique!")
    