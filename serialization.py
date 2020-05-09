from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.UUID()
    name = fields.String(required=True, validate=validate.Length(min=3, max=33))
    age = fields.Integer(required=True, strict=True, validate=validate.Range(min=0, max=99))
