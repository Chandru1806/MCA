from marshmallow import Schema, fields, validate

class PreferenceSchema(Schema):
    phone = fields.Str(validate=validate.Length(max=15))
    address_line_1 = fields.Str(validate=validate.Length(max=255))
    address_line_2 = fields.Str(validate=validate.Length(max=255))
    city = fields.Str(validate=validate.Length(max=50))
    state = fields.Str(validate=validate.Length(max=50))
