from odoo import fields, api, models


class BookingWizard(models.TransientModel):
    _name = 'booking.wizard'
    _description = 'Create Booking While Property on Sale'

    customer_id = fields.Many2one('res.partner', string='Customer', domain=[('user_type', '=', 'customer')])
    property_id = fields.Many2one('property.details', string='Property')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    book_price = fields.Monetary(related="property_id.token_amount", string="Book Price")
    ask_price = fields.Monetary(string="Ask Price")

    is_any_broker = fields.Boolean(string='Any Broker?')
    broker_id = fields.Many2one('res.partner', string='Broker', domain=[('user_type', '=', 'broker')])
    commission_type = fields.Selection([('f', 'Fix'), ('p', 'Percentage')], string="Commission Type")
    broker_commission = fields.Monetary(string='Commission')
    broker_commission_percentage = fields.Float(string='Percentage')
    commission_from = fields.Selection([('customer', 'Customer'), ('landlord', 'Landlord',)], default='customer',
                                       string="Commission From")

    def create_booking_action(self):
        data = {
            'customer_id': self.customer_id.id,
            'property_id': self.property_id.id,
            'ask_price': self.ask_price,
            'is_any_broker': self.is_any_broker,
            'broker_id': self.broker_id.id,
            'commission_type': self.commission_type,
            'broker_commission': self.broker_commission,
            'broker_commission_percentage': self.broker_commission_percentage,
            'stage': 'booked',
            'commission_from': self.commission_from
        }
        self.env['property.vendor'].create(data)
