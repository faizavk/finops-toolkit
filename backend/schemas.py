"""Input validation schemas for API endpoints"""
from marshmallow import Schema, fields, validate, ValidationError

class ForecastRequestSchema(Schema):
    """Schema for forecast endpoint"""
    train_ratio = fields.Float(
        required=False,
        validate=validate.Range(min=0.1, max=0.9),
        missing=0.8,
        error_messages={
            'required': 'train_ratio is required',
            'invalid': 'train_ratio must be between 0.1 and 0.9'
        }
    )
    periods = fields.Int(
        required=False,
        validate=validate.Range(min=1, max=365),
        missing=30,
        error_messages={
            'invalid': 'periods must be between 1 and 365'
        }
    )
    sensitivity = fields.Str(
        required=False,
        validate=validate.OneOf(['Low', 'Medium', 'High']),
        missing='Medium',
        error_messages={
            'invalid': 'sensitivity must be Low, Medium, or High'
        }
    )

class AnomalyRequestSchema(Schema):
    """Schema for anomaly detection endpoint"""
    sensitivity = fields.Str(
        required=False,
        validate=validate.OneOf(['Low', 'Medium', 'High']),
        missing='Medium',
        error_messages={
            'invalid': 'sensitivity must be Low, Medium, or High'
        }
    )
    periods = fields.Int(
        required=False,
        validate=validate.Range(min=1, max=365),
        missing=30,
        error_messages={
            'invalid': 'periods must be between 1 and 365'
        }
    )

class ServiceForecastRequestSchema(Schema):
    """Schema for service forecast endpoint"""
    periods = fields.Int(
        required=False,
        validate=validate.Range(min=1, max=365),
        missing=30,
        error_messages={
            'invalid': 'periods must be between 1 and 365'
        }
    )

