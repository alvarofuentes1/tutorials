from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RealEstateType(models.Model):
    _name = "real_estate_type"
    _description = "Tipos de casas"
    _order = "name"

    
    name = fields.Char(required=True, string="Name")
    property_ids = fields.One2many("real_estate", "property_type", string="Properties")
    sequence = fields.Integer(default=10)
    offer_ids = fields.One2many('real_estate_offer', 'property_type_id', string='offer')
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        # Contador = numero de ofertas
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
    
    @api.constrains("name")
    def _check_unique_name(self):
        for type in self:
            existing_types = self.search([
                ("id", "!=", type.id),
                ("name", "ilike", type.name) #ilike realiza una busqueda sin tener en cuenta minusculas y mayusculas
            ])
            if existing_types:
                raise ValidationError("The property type name must be unique!")
    
    def action_view_offers(self):
        """ Opens the real_estate_type list filtered by property_type_id """
        return {
            "type": "ir.actions.act_window",
            "name": "Offers",
            "res_model": "real_estate_offer",
            "view_mode": "list,form",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id},
        }