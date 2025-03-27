
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class RealEstate(models.Model):
    _name = "real_estate"
    _description = "Propiedades(casas)"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=1)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    property_type = fields.Many2one("real_estate_type")
    property_salesperson = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    property_buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("real_estate_tag")
    offer_ids = fields.One2many("real_estate_offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new')

    def action_set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("A canceled property cannot be sold.")
            record.state = 'sold'

    def action_set_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be canceled.")
            record.state = 'canceled'
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area
            
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped('price')) if property.offer_ids else 0
            
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:  
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False 
            
    @api.constrains("expected_price", "selling_price")
    def _check_prices(self):
        for property in self:
            if property.expected_price <= 0:
                raise ValidationError("The expected price must be strictly positive!")
            if property.selling_price and property.selling_price < property.expected_price*0.9:
                raise ValidationError("The selling price must be al least 90% of the expected price!")
            
    def unlink(self):
        for property in self:
            if property.state not in ('new', 'canceled'):
                raise UserError("You can only delete properties that are in 'New' or 'Cancelled' state.")
        return super(RealEstate, self).unlink()