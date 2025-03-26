from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PropertyTag(models.Model):
    _name = "real_estate_tag"
    _description = "Etiquetas de la propiedad"
    _order = "name"
    
    name = fields.Char(required=True)
    
    @api.constrains("name")
    def _check_unique_name(self):
        for tag in self:
            existing_types = self.search([
                ("id", "!=", tag.id),
                ("name", "ilike", tag.name) #ilike realiza una busqueda sin tener en cuenta minusculas y mayusculas
            ])
            if existing_types:
                raise ValidationError("The property type name must be unique!")
    