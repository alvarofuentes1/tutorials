from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "real_estate",  # Modelo relacionado (estate.property)
        "property_salesperson",  # Campo inverso en estate.property
        string="Properties",
        domain=[("state", "=", "new")]  # Solo propiedades disponibles
    )