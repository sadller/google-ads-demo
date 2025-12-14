from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date


class CampaignSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=255))
    objective = fields.String(required=True)
    campaign_type = fields.String(required=True)
    daily_budget = fields.Integer(required=True, validate=validate.Range(min=1000000))
    start_date = fields.Date(required=True)
    end_date = fields.Date(allow_none=True)
    status = fields.String(dump_only=True)
    ad_group_name = fields.String(required=True, validate=validate.Length(min=1, max=255))
    ad_headline = fields.String(required=True, validate=validate.Length(min=1, max=255))
    ad_description = fields.String(required=True, validate=validate.Length(min=1, max=500))
    final_url = fields.URL(required=True)
    asset_url = fields.URL(allow_none=True)
    google_campaign_id = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('start_date')
    def validate_start_date(self, value):
        if value < date.today():
            raise ValidationError("Start date cannot be in the past")


campaign_schema = CampaignSchema()
campaigns_schema = CampaignSchema(many=True)
