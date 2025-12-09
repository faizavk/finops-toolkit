"""Authentication and authorization utilities"""
import os
from functools import wraps
from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)

# API Keys - In production, store in database or secret manager
# Load from environment variables
VALID_API_KEYS = set()
api_key_1 = os.getenv('API_KEY_1', 'dev-key-12345')
api_key_2 = os.getenv('API_KEY_2', 'dev-key-67890')

if api_key_1:
    VALID_API_KEYS.add(api_key_1)
if api_key_2:
    VALID_API_KEYS.add(api_key_2)

# For development, allow requests without API key
# Set REQUIRE_API_KEY=false to disable in development
# DEFAULT: false (no API key required)
REQUIRE_API_KEY = os.getenv('REQUIRE_API_KEY', 'false').lower() == 'true'

def require_api_key(f):
    """Decorator to require API key for protected endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not REQUIRE_API_KEY:
            # Development mode - allow without API key
            return f(*args, **kwargs)
        
        api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not api_key:
            logger.warning(f"API access denied - No API key provided - IP: {request.remote_addr}")
            return jsonify({
                'error': 'API key required',
                'message': 'Please provide an API key in X-API-Key header or Authorization header'
            }), 401
        
        if api_key not in VALID_API_KEYS:
            logger.warning(f"API access denied - Invalid API key - IP: {request.remote_addr}")
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is not valid'
            }), 401
        
        # Log successful authentication
        logger.info(f"API access granted - IP: {request.remote_addr}")
        return f(*args, **kwargs)
    
    return decorated_function

def get_api_key_from_request():
    """Extract API key from request headers"""
    return request.headers.get('X-API-Key') or request.headers.get('Authorization', '').replace('Bearer ', '')

