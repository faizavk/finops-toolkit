# FinOps Toolkit - Complete Tech Stack Summary

## 🏗️ Architecture Overview

**Type**: Full-Stack Web Application  
**Pattern**: RESTful API (Backend) + Single Page Application (Frontend)  
**Deployment**: Local Development (can be containerized)

---

## 🔵 Backend Tech Stack

### Core Framework
- **Flask 3.0.0** - Python web framework for REST API
- **Python 3.10.6** - Programming language

### API & Communication
- **Flask-CORS 4.0.0** - Cross-Origin Resource Sharing for API access
- **RESTful API** - JSON-based API endpoints

### Security & Authentication
- **Flask-Limiter 3.5.0** - Rate limiting for API endpoints
- **Marshmallow 3.20.1** - Input validation and schema validation
- **Python-dotenv 1.0.0** - Environment variable management
- **Custom Auth Module** - API key authentication system
- **Secure HTTP Headers** - X-Content-Type-Options, X-Frame-Options, CSP, etc.
- **Audit Logging** - Rotating file handler for security logs

### Data Processing & Analysis
- **Pandas 2.1.4** - Data manipulation and analysis
- **NumPy 1.26.2** - Numerical computing and array operations

### Machine Learning
- **Prophet 1.1.5** - Facebook's time series forecasting library
  - Built on **Stan** (probabilistic programming language)
  - Uses **cmdstanpy** - Python interface to CmdStan
  - Requires **cmdstan** - Stan compiler

### Data Format
- **CSV** - Input data format
- **JSON** - API response format

### Date/Time Handling
- **python-dateutil 2.8.2** - Date parsing and manipulation

### Production Server
- **Gunicorn 21.2.0** - Production WSGI HTTP Server for Unix

### Development Tools
- **Virtual Environment (venv)** - Python dependency isolation

---

## 🟢 Frontend Tech Stack

### Core Framework
- **React 18.2.0** - JavaScript UI library
- **React DOM 18.2.0** - React rendering for web

### Build Tools
- **React Scripts 5.0.1** - Create React App build configuration
  - Webpack (bundler)
  - Babel (JavaScript compiler)
  - ESLint (code linting)

### Data Visualization
- **Recharts 2.10.3** - React charting library
  - Built on D3.js
  - Components: LineChart, AreaChart, ComposedChart
  - Features: ResponsiveContainer, Tooltips, Legends, Gradients

### HTTP Client
- **Axios 1.6.2** - Promise-based HTTP client for API calls

### UI/UX Enhancements
- **React Toastify 9.1.3** - Toast notification system

### Styling
- **CSS3** - Custom styling
  - Flexbox & Grid layouts
  - CSS Gradients
  - Responsive design
  - Custom animations

### Development
- **Node.js v20.11.1** - JavaScript runtime
- **npm 10.2.4** - Package manager

---

## 📊 Data Flow Architecture

```
CSV File → Pandas DataFrame → Prophet Model → Forecast → JSON API → React Components → Recharts Visualization
```

### Data Pipeline:
1. **Data Loading**: CSV → Pandas DataFrame
2. **Data Processing**: Aggregation, grouping, date parsing
3. **ML Training**: Prophet model training on time series
4. **Forecasting**: Future predictions with confidence intervals
5. **Anomaly Detection**: Statistical comparison with thresholds
6. **API Response**: JSON serialization
7. **Frontend Rendering**: React components with Recharts

---

## 🗄️ Data Storage

- **File-based**: CSV files for input data
- **In-memory**: Global variables for model state
- **Output**: CSV files for service forecasts (long & wide format)

---

## 🔧 Development Environment

### Backend
- **Python Virtual Environment** - Dependency isolation
- **Flask Development Server** - Built-in WSGI server
- **Debug Mode** - Enabled for development

### Frontend
- **React Development Server** - Hot module replacement
- **Webpack Dev Server** - Development bundling
- **Browser DevTools** - Debugging and inspection

---

## 📦 Key Dependencies Breakdown

### Backend Dependencies (Python)
```
flask==3.0.0              # Web framework
flask-cors==4.0.0         # CORS middleware
pandas==2.1.4             # Data processing
numpy==1.26.2             # Numerical computing
prophet==1.1.5            # Time series forecasting
python-dateutil==2.8.2    # Date utilities
gunicorn==21.2.0          # Production WSGI server
flask-limiter==3.5.0      # Rate limiting
marshmallow==3.20.1       # Input validation
python-dotenv==1.0.0      # Environment variables
```

### Frontend Dependencies (JavaScript)
```json
{
  "react": "^18.2.0",           // UI framework
  "react-dom": "^18.2.0",       // React rendering
  "react-scripts": "5.0.1",      // Build tools
  "recharts": "^2.10.3",         // Charts
  "axios": "^1.6.2",             // HTTP client
  "react-toastify": "^9.1.3"    // Notifications
}
```

---

## 🎨 UI/UX Technologies

- **Responsive Design** - Mobile-friendly layouts
- **CSS Grid & Flexbox** - Layout systems
- **CSS Gradients** - Visual enhancements
- **CSS Animations** - Loading spinners, transitions
- **Modern Color Palette** - Purple/blue gradient theme

---

## 🔐 Security & Best Practices

### Implemented Security Features:
- **Rate Limiting** - Flask-Limiter with configurable limits per endpoint
  - Default: 200/day, 50/hour per IP
  - Forecast/Anomalies: 10/minute
  - Service Forecast: 5/minute
- **Input Validation** - Marshmallow schemas for all POST endpoints
  - Type checking, range validation, enum validation
- **API Key Authentication** - Optional in dev, required in production
  - Supports X-API-Key header or Authorization Bearer token
  - Custom decorator: `@require_api_key`
- **Secure HTTP Headers** - All responses include:
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: SAMEORIGIN
  - Referrer-Policy: strict-origin-when-cross-origin
  - Content-Security-Policy
  - Strict-Transport-Security
- **Audit Logging** - Rotating file handler (10MB, 5 backups)
  - Logs all API requests, authentication attempts, errors
  - Location: `backend/logs/audit.log`
- **Error Handling** - Comprehensive error handlers (400, 401, 403, 404, 429, 500)
  - Security: Error messages don't leak sensitive information
- **Path Traversal Protection** - File download endpoint validates filenames
- **CORS** - Configured for cross-origin requests with environment-based origins
- **Environment Variables** - Secrets management via .env files
- **Virtual Environments** - Dependency isolation
- **Environment Separation** - Development vs Production ready

---

## 📈 Machine Learning Stack

### Prophet Library Components:
- **Stan Backend** - Statistical modeling engine
- **CmdStan** - Stan compiler
- **Seasonality Detection** - Yearly, weekly patterns
- **Uncertainty Intervals** - Confidence bounds (95%)
- **Trend Analysis** - Linear growth modeling

### ML Features Implemented:
- Time series forecasting
- Anomaly detection (statistical thresholds)
- Service-level forecasting
- Proportional distribution fallback

---

## 🚀 Deployment Readiness

### Current Setup:
- ✅ Local development servers
- ✅ Virtual environments
- ✅ Dependency management
- ✅ Error handling
- ✅ CORS configuration

### Production Ready:
- ✅ Production WSGI server (Gunicorn)
- ✅ Rate limiting
- ✅ Input validation
- ✅ API key authentication
- ✅ Secure headers
- ✅ Audit logging
- ✅ Error handling
- ✅ Environment variable management

### Can Be Extended To:
- Docker containerization
- Cloud deployment (AWS, GCP, Azure, Render)
- Database integration (PostgreSQL, MongoDB)
- Advanced authentication (JWT, OAuth)
- Session management
- Two-factor authentication

---

## 📊 Technology Summary Table

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Backend Language** | Python | 3.10.6 | Server-side logic |
| **Backend Framework** | Flask | 3.0.0 | Web API framework |
| **Production Server** | Gunicorn | 21.2.0 | WSGI HTTP server |
| **Frontend Framework** | React | 18.2.0 | UI library |
| **Data Processing** | Pandas | 2.1.4 | Data manipulation |
| **ML Library** | Prophet | 1.1.5 | Time series forecasting |
| **Charts** | Recharts | 2.10.3 | Data visualization |
| **HTTP Client** | Axios | 1.6.2 | API communication |
| **Notifications** | React Toastify | 9.1.3 | User feedback |
| **Rate Limiting** | Flask-Limiter | 3.5.0 | API rate limiting |
| **Input Validation** | Marshmallow | 3.20.1 | Schema validation |
| **Environment Vars** | Python-dotenv | 1.0.0 | Config management |
| **Build Tool** | React Scripts | 5.0.1 | Frontend bundling |
| **Runtime** | Node.js | 20.11.1 | JavaScript execution |

---

## 🎯 Key Technologies by Feature

### Forecasting
- **Prophet** - Time series forecasting
- **Pandas** - Data aggregation
- **NumPy** - Statistical calculations

### Visualization
- **Recharts** - Interactive charts
- **React** - Component rendering
- **CSS** - Styling and animations

### API Communication
- **Flask** - REST API endpoints
- **Axios** - HTTP requests
- **JSON** - Data serialization

### Data Management
- **Pandas** - DataFrame operations
- **CSV** - File I/O
- **Python datetime** - Date handling

---

## 💡 Why These Technologies?

1. **Flask** - Lightweight, flexible, perfect for REST APIs
2. **React** - Component-based, great for interactive dashboards
3. **Prophet** - Industry-standard for time series forecasting
4. **Recharts** - Easy-to-use, React-native charting
5. **Pandas** - Powerful data manipulation for cost analysis
6. **Axios** - Simple, promise-based HTTP client

---

## 📝 Development Workflow

```
Backend (Python/Flask) ←→ Frontend (React)
     ↓                        ↓
  CSV Data              User Interface
     ↓                        ↓
  Prophet ML            Recharts Charts
     ↓                        ↓
  JSON API              Interactive Dashboard
```

---

**Total Technologies**: ~20 core technologies  
**Lines of Code**: ~3,000+ (Backend + Frontend + Security)  
**Dependencies**: 25+ packages  
**Architecture**: Modern full-stack web application with enterprise security  
**Security Features**: 8+ implemented security measures

