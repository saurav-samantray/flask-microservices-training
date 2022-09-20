from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf


class AddressSchema(Schema):
    id = fields.Int()
    address_line_1 = fields.Str(required=True, validate=Length(max=50))
    city = fields.Str(required=True)
    state = fields.Str(required=True, validate=OneOf(choices= ['KA', 'TG', 'OD', 'WB', 'DL', 'TN', 'KL', 'MH', 'GJ', 'RJ', 'MP', 'AS', 'UP', 'BH']))
    pin = fields.Int(required=True)