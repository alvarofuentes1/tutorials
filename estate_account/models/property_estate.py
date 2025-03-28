from odoo import models, fields, Command

class PropertyEstate(models.Model):
    _inherit = "real_estate"
    
    def action_set_sold(self):
        print("Método action_set_sold sobrescrito desde estate_account")
      
        # Crear una factura (account.move) con los datos de la propiedad
        for real_estate in self:
            self.env['account.move'].create({
                'partner_id': real_estate.property_buyer.id,
                'move_type': 'out_invoice',  # Factura de cliente
                'invoice_line_ids': [
                    Command.create({
                        'name': "Commission (6%)",
                        'quantity': 1,
                        'price_unit': real_estate.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': "Administrative Fees",
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            })
        
        return super().action_set_sold()