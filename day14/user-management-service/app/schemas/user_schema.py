from marshmallow import Schema, fields
from marshmallow.validate import Length, Range, OneOf


class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=Length(max=30))
    email = fields.Str(required=True)
    age = fields.Int(required=True, validate=Range(min=16, max=100))
    password = fields.Str(required=True)
    role = fields.Str(validate=OneOf(['ADMIN', 'USER']))