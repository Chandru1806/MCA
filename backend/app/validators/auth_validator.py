from marshmallow import Schema, fields, validate, EXCLUDE

class SignupSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, validate=validate.Length(min=8))

class UpdateUserSchema(Schema):
    first_name = fields.Str(validate=validate.Length(min=1, max=100))
    last_name = fields.Str(validate=validate.Length(min=1, max=100))
    email = fields.Email()
    password = fields.Str(validate=validate.Length(min=8))
    address_line_1 = fields.Str(validate=validate.Length(max=255))
    address_line_2 = fields.Str(validate=validate.Length(max=255))

class RefreshTokenSchema(Schema):
    refresh_token = fields.Str(required=True)
