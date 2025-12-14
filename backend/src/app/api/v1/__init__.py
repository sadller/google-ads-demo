"""
API Version 1
Main API blueprint for version 1
"""
from flask import Blueprint

# Create API v1 blueprint
api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Import all endpoints to register routes
from .endpoints import health, campaigns

__all__ = ['api_v1_bp']
