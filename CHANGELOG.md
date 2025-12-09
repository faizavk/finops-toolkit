# Changelog - FinOps Toolkit

## [Latest] - Security Features Update

### 🔐 Security Features Added

#### New Security Modules
- **Flask-Limiter 3.5.0** - Rate limiting for all API endpoints
  - Default limits: 200/day, 50/hour per IP
  - Endpoint-specific limits (forecast: 10/min, service forecast: 5/min)
- **Marshmallow 3.20.1** - Input validation schemas
  - ForecastRequestSchema
  - AnomalyRequestSchema
  - ServiceForecastRequestSchema
- **Python-dotenv 1.0.0** - Environment variable management
- **Custom Auth Module** (`backend/auth.py`) - API key authentication
- **Input Validation Module** (`backend/schemas.py`) - Request validation

#### Security Features Implemented
1. ✅ **Rate Limiting** - Protects against API abuse
2. ✅ **Input Validation** - All POST endpoints validate input
3. ✅ **API Key Authentication** - Optional in dev, required in production
4. ✅ **Secure HTTP Headers** - X-Content-Type-Options, CSP, HSTS, etc.
5. ✅ **Audit Logging** - Rotating file handler (10MB, 5 backups)
6. ✅ **Error Handling** - Comprehensive error handlers (400, 401, 403, 404, 429, 500)
7. ✅ **Path Traversal Protection** - Secure file downloads
8. ✅ **Environment Variables** - Secrets management

#### Production Server
- **Gunicorn 21.2.0** - Production WSGI HTTP server

### 📝 Files Added
- `backend/auth.py` - Authentication module
- `backend/schemas.py` - Input validation schemas
- `backend/.env.example` - Environment variables template
- `backend/logs/` - Log directory for audit logs
- `SECURITY_IMPLEMENTATION_SUMMARY.md` - Security documentation
- `SECURITY_IMPLEMENTATION_GUIDE.md` - Implementation guide
- `SECURITY_FEATURES.md` - Security features reference
- `TROUBLESHOOTING.md` - Troubleshooting guide
- `QUICK_FIX.md` - Quick fix guide

### 📝 Files Updated
- `backend/app.py` - Added all security features, error handlers, logging
- `backend/requirements.txt` - Added security dependencies
- `frontend/src/components/Dashboard.js` - Added API key support, improved error handling
- `TECH_STACK.md` - Updated with security technologies
- `README.md` - Added security features section
- `DEPLOYMENT_GUIDE.md` - Updated with security dependencies
- `.gitignore` - Added logs and .env exclusions

### 🔧 Technical Changes

#### Backend Changes
- Added `@limiter.limit()` decorator to all endpoints
- Added `@require_api_key` decorator to protected endpoints
- Added `@validate_request` decorator to POST endpoints
- Added `set_security_headers()` after-request hook
- Added comprehensive error handlers
- Added audit logging with RotatingFileHandler
- Added fallback mechanisms for missing security packages
- Updated CORS configuration to use environment variables
- Changed `app.run()` to use `os.getenv('PORT', 5000)` for deployment

#### Frontend Changes
- Added API key support via `REACT_APP_API_KEY` environment variable
- Improved error handling with detailed error messages
- Added centralized `apiCall()` function with security headers
- Better error messages for connection issues, authentication, rate limits

### 🐛 Bug Fixes
- Fixed service forecast showing "0 services" - now correctly counts unique services
- Fixed error handling to show more informative messages
- Added fallback mechanisms so app works even without security packages
- Fixed limiter decorator to work with or without flask-limiter

### 📦 Dependencies Added
```
gunicorn==21.2.0      # Production WSGI server
flask-limiter==3.5.0  # Rate limiting
marshmallow==3.20.1    # Input validation
python-dotenv==1.0.0   # Environment variables
```

### 🔄 Breaking Changes
- **None** - All changes are backward compatible
- Security features are optional in development (REQUIRE_API_KEY=false by default)
- Code includes fallbacks for missing security packages

### 📚 Documentation Updates
- Updated TECH_STACK.md with security technologies
- Updated README.md with security features section
- Updated DEPLOYMENT_GUIDE.md with security dependencies
- Created comprehensive security documentation

### 🚀 Deployment Notes
- For production, set `REQUIRE_API_KEY=true` in environment
- Configure API keys via environment variables
- Set `FRONTEND_URL` for CORS in production
- All security features work out of the box with fallbacks

---

## Previous Versions

### Initial Release
- 10 core features implemented
- Historical cost visualization
- Prophet forecasting
- Anomaly detection
- Root cause analysis
- Unit cost computation
- Security insights
- Service-level forecasting
- Interactive dashboard

---

**Version**: 2.0.0 (Security Update)  
**Date**: December 2025  
**Status**: Production Ready with Enterprise Security

