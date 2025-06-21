from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    role = fields.Str(validate=validate.OneOf(['manager','employee']))

class FeedbackSchema(Schema):
    id = fields.Int(dump_only=True)
    manager_id = fields.Int(required=True)
    employee_id = fields.Int(required=True)
    strengths = fields.Str(required=True)
    improvements = fields.Str(required=True)
    sentiment = fields.Str(validate=validate.OneOf(['positive','neutral','negative']), required=True)
    tags = fields.List(fields.Str(), load_default=[])
    anonymous = fields.Bool(load_default=False)
    created_at = fields.DateTime(dump_only=True)
    acknowledged = fields.Bool()
    employee_comments = fields.Str(allow_none=True)