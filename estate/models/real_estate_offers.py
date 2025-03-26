from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class PropertyOffer(models.Model):
    _name = "real_estate_offer"
    _description = "Ofertas hechas por la propiedad"
    
    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused","Refused")
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("real_estate", required=True)
    validity = fields.Integer(default="7")
    date_deadline = fields.Date(compute="_compute_set_deadline", inverse="_inverse_set_deadline")
    
    @api.depends("validity")
    def _compute_set_deadline(self):
        for property in self:
            property.date_deadline = fields.Date.today() + relativedelta(days=property.validity)
            
    def _inverse_set_deadline(self):
            for property in self:
                property.validity = (property.date_deadline - fields.Date.today()).days