# 🔒 Security Implementation Guide - Step by Step

## 🎯 Quick Implementation Guide

This guide shows you how to add the most important security features to your FinOps Toolkit.

---

## 🔴 PRIORITY 1: Rate Limiting (15 minutes)

### Step 1: Install Package
```bash
cd backend
source venv/bin/activate
pip install flask-limiter
```

### Step 2: Update requirements.txt
Add: `flask-limiter==3.5.0`

### Step 3: Add to app.py
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Apply to specific endpoints
@app.route('/api/forecast', methods=['POST'])
@limiter.limit("10 per minute")
def get_forecast():
    # ... existing code
```

**Benefits:** Prevents API abuse and DDoS attacks

---

## 🔴 PRIORITY 2: Input Validation (30 minutes)

### Step 1: Install Package
```bash
pip install marshmallow
```

### Step 2: Create validation schemas
Create `backend/schemas.py`:
```python
from marshmallow import Schema, fields, validate, ValidationError

class ForecastRequestSchema(Schema):
    train_ratio = fields.Float(
        required=True,
        validate=validate.Range(min=0.1, max=0.9),
        error_messages={'required': 'train_ratio is required'}
    )
    periods = fields.Int(
        required=False,
        validate=validate.Range(min=1, max=365),
        missing=30
    )
    sensitivity = fields.Str(
        required=False,
        validate=validate.OneOf(['Low', 'Medium', 'High']),
        missing='Medium'
    )

class AnomalyRequestSchema(Schema):
    sensitivity = fields.Str(
        required=False,
        validate=validate.OneOf(['Low', 'Medium', 'High']),
        missing='Medium'
    )
    periods = fields.Int(
        required=False,
        validate=validate.Range(min=1, max=365),
        missing=30
    )
```

### Step 3: Use in endpoints
```python
from schemas import ForecastRequestSchema

@app.route('/api/forecast', methods=['POST'])
@limiter.limit("10 per minute")
def get_forecast():
    schema = ForecastRequestSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    train_ratio = data['train_ratio']
    periods = data.get('periods', 30)
    sensitivity = data.get('sensitivity', 'Medium')
    # ... rest of code
```

**Benefits:** Prevents injection attacks and invalid data

---

## 🔴 PRIORITY 3: Secure Headers (10 minutes)

### Add to app.py
```python
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response
```

**Benefits:** Prevents clickjacking, XSS, and other attacks

---

## 🔴 PRIORITY 4: Environment Variables (5 minutes)

### Step 1: Install python-dotenv
```bash
pip install python-dotenv
```

### Step 2: Create .env file (for local)
Create `backend/.env`:
```
API_KEY=your-secret-api-key-here
DEBUG=False
SECRET_KEY=your-secret-key-for-sessions
```

### Step 3: Update app.py
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

# Use environment variables
API_KEY = os.getenv('API_KEY', 'default-key-for-dev')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```

### Step 4: Add to .gitignore
```
backend/.env
```

**Benefits:** Secrets not in code, different configs for dev/prod

---

## 🟡 PRIORITY 5: Basic API Key Authentication (1 hour)

### Step 1: Create auth module
Create `backend/auth.py`:
```python
import os
from functools import wraps
from flask import request, jsonify

# In production, store in database or secret manager
VALID_API_KEYS = {
    os.getenv('API_KEY_1', 'key1'),
    os.getenv('API_KEY_2', 'key2'),
}

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key not in VALID_API_KEYS:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function
```

### Step 2: Protect endpoints
```python
from auth import require_api_key

@app.route('/api/forecast', methods=['POST'])
@require_api_key
@limiter.limit("10 per minute")
def get_forecast():
    # ... existing code
```

### Step 3: Frontend - Add API key
In `frontend/src/components/Dashboard.js`:
```javascript
const API_KEY = process.env.REACT_APP_API_KEY || '';

const apiCall = async (url, options = {}) => {
  return axios({
    ...options,
    url: `${API_BASE}${url}`,
    headers: {
      'X-API-Key': API_KEY,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
};
```

**Benefits:** Control who can access your API

---

## 🟡 PRIORITY 6: Audit Logging (30 minutes)

### Step 1: Setup logging
Add to `app.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/audit.log', maxBytes=10000000, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_api_access(endpoint, method, user=None, ip=None):
    """Log API access for audit trail"""
    logger.info(f"API Access - {method} {endpoint} - User: {user} - IP: {ip}")

@app.before_request
def log_request():
    log_api_access(
        request.endpoint,
        request.method,
        user=request.headers.get('X-API-Key', 'anonymous'),
        ip=request.remote_addr
    )
```

### Step 2: Create logs directory
```bash
mkdir -p backend/logs
echo "*.log" >> .gitignore
```

**Benefits:** Track who accessed what and when

---

## 🟡 PRIORITY 7: Error Handling (20 minutes)

### Secure error responses
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded', 'retry_after': str(e.description)}), 429
```

**Benefits:** Don't leak sensitive info in error messages

---

## 🔍 SECURITY TESTING

### 1. Dependency Scanning
```bash
# Backend
pip install safety
safety check

# Frontend
npm audit
npm audit fix
```

### 2. Code Security Scanning
```bash
pip install bandit
bandit -r backend/
```

### 3. Manual Testing
- Try invalid inputs
- Test rate limits
- Test without API key
- Test with wrong API key

---

## 📋 UPDATED REQUIREMENTS.TXT

After implementing security features:
```
flask==3.0.0
flask-cors==4.0.0
pandas==2.1.4
numpy==1.26.2
prophet==1.1.5
python-dateutil==2.8.2
gunicorn==21.2.0
flask-limiter==3.5.0
marshmallow==3.20.1
python-dotenv==1.0.0
```

---

## ✅ SECURITY CHECKLIST

After implementation:

- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] Secure headers added
- [ ] Environment variables for secrets
- [ ] API key authentication (optional)
- [ ] Audit logging implemented
- [ ] Error handling secure
- [ ] Dependencies scanned
- [ ] .env in .gitignore
- [ ] HTTPS enforced (Render does this)

---

## 🎯 RECOMMENDED IMPLEMENTATION ORDER

1. **Week 1:** Rate Limiting + Secure Headers (Quick wins)
2. **Week 2:** Input Validation + Error Handling
3. **Week 3:** Environment Variables + API Keys
4. **Week 4:** Audit Logging + Testing

---

**Start with the quick wins, then gradually add more security features!** 🔒

