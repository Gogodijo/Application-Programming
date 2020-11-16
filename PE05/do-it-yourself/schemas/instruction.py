from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError

from schemas.user import UserSchema

def validateDuration(n):
    if n < 1:
        raise ValidationError("Duration must be larger than 1")

def validateCost(n):
    if n < 0:
        raise ValidationError("Cost can't be negative")

class InstructionSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(validate=[validate.Length(max=200)])
    steps = fields.List(fields.String())
    tools = fields.List(fields.String())
    cost = fields.Integer(validate=validateCost)
    duration = fields.Integer(validate=validateDuration)
    author = fields.Nested(UserSchema, attribute='user', dump_only=True,
        only=["id","username"])
    is_publish = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self,data,many, **kwargs):
        if many:
            return {'data': data}
        return data