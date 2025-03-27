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
    property_type_id = fields.Many2one("real_estate_type", related='property_id.property_type', store=True)
    
    def action_accept(self):
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError("You cannot accept an offer for a sold property.")
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'
            
            other_offers = offer.property_id.offer_ids - offer
            other_offers.write({'status': 'refused'})

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
            
            # Verificar si quedan ofertas aceptadas
            accepted_offers = offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
        
            # Si no hay ofertas aceptadas, cambiar el estado a "offer_received"
            if not accepted_offers:
                offer.property_id.state = 'offer_received'
    
    @api.model_create_multi
    def create(self, vals_list):
        # Si es un solo dict (caso más común), lo convertimos en lista
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        new_records = []
        for vals in vals_list:
            property_id = self.env["real_estate"].browse(vals["property_id"])
            # ... haz lo que tengas que hacer aquí ...
            new_record = super().create(vals)
            new_records.append(new_record)

        return new_records[0] if len(new_records) == 1 else new_records
    
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
            
    @api.constrains("property_id")
    def _check_property_state(self):
        for offer in self:
            if offer.property_id.state in ["offer_accepted", "sold", "canceled"]:
                raise ValidationError("You cannot add an offer when the property is in 'Offer Accepted', 'Sold', or 'Canceled' state.")