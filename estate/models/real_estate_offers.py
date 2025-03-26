from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class PropertyOffer(models.Model):
    _name = "real_estate_offer"
    _description = "Ofertas hechas por la propiedad"
    _order = "price desc"
    
    price = fields.Float()
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("real_estate", required=True)
    validity = fields.Integer(default="7")
    date_deadline = fields.Date(compute="_compute_set_deadline", inverse="_inverse_set_deadline")
    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], default='pending')
    
    def action_accept(self):
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError("You cannot accept an offer for a sold property.")
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_received'
            
            other_offers = offer.property_id.offer_ids - offer
            other_offers.write({'status': 'refused'})

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
    
    @api.depends("validity")
    def _compute_set_deadline(self):
        for property in self:
            property.date_deadline = fields.Date.today() + relativedelta(days=property.validity)
            
    def _inverse_set_deadline(self):
            for property in self:
                property.validity = (property.date_deadline - fields.Date.today()).days
                
    @api.constrains("price")
    def _check_prices(self):
        for offer in self:
            if offer.price <= 0:
                raise ValidationError("The offer price must be strictly positive!")