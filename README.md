# FinOps Toolkit - Complete Project

A comprehensive cloud cost management and forecasting dashboard with 10 core features.

## 🟦 Features Checklist (All 10 Features Implemented)

✔ **1. Historical Cost Visualization** - Chart of actual daily cloud costs  
✔ **2. Future Forecasting with Prophet** - Predicts next N days (default 30) with yhat, yhat_upper, yhat_lower and future shaded region  
✔ **3. Customizable Train/Test Ratio** - Select 60:40 / 70:30 / 80:20 from UI, backend retrains Prophet model  
✔ **4. Sensitivity Slider** - Controls anomaly detection strictness (Low/Medium/High)  
✔ **5. Anomaly Detection** - Compares historical actual cost with Prophet upper bound × sensitivity factor  
✔ **6. Root Cause Analysis (RCA)** - For each anomaly date: Top services, Top regions, Top tags (displayed in modal popup)  
✔ **7. Unit Cost Computation** - Computes unit_cost = cost / units (or cost per service/region/tag if no units column)  
✔ **8. Security Insights** - Shows extreme cost spikes (actual > 10× predicted) and rare/new tags  
✔ **9. Service-Level Forecast** - Forecasts per service using Prophet (with fallback to proportional distribution), outputs forecast_service_long.csv and forecast_service_wide.csv  
✔ **10. Complete Interactive Frontend** - Dashboard with Load Forecast, Load Anomalies, Retrain Model, Security analysis, RCA modal, Toasts, Loading overlay, and Future shading on forecast graph

## 📁 Project Structure

```
fin/
├── backend/
│   ├── app.py              # Flask API with all endpoints
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   ├── Dashboard.js
│   │   │   ├── CostChart.js
│   │   │   ├── ForecastChart.js
│   │   │   ├── AnomaliesTable.js
│   │   │   ├── RCAModal.js
│   │   │   └── SecurityInsights.js
│   │   └── index.js
│   └── package.json
├── outputs/                # Generated CSV files
│   ├── forecast_service_long.csv
│   └── forecast_service_wide.csv
├── ideal_cost_data.csv     # Input data
└── README.md
```

## 🚀 Quick Start

### Option 1: Using Start Scripts (Recommended)

**Terminal 1 - Backend:**
```bash
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
```

### Option 2: Manual Setup

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note:** The project includes security features. If you encounter import errors for `flask-limiter`, `marshmallow`, or `python-dotenv`, the code includes fallbacks and will work without them. For full security features, ensure all dependencies are installed.

4. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## 📊 API Endpoints

All endpoints (except `/api/health`) are protected with:
- Rate limiting (configurable per endpoint)
- API key authentication (optional in dev, required in production)
- Input validation (POST endpoints)

**Endpoints:**
- `GET /api/health` - Health check (no auth required)
- `GET /api/historical` - Get historical cost data
- `POST /api/forecast` - Generate forecast (requires train_ratio, periods, sensitivity)
- `POST /api/anomalies` - Detect anomalies (requires sensitivity, periods)
- `GET /api/rca/<date>` - Get RCA for specific anomaly date
- `GET /api/unit-costs` - Compute unit costs
- `GET /api/security` - Get security insights
- `POST /api/service-forecast` - Generate service-level forecasts
- `GET /api/download/<filename>` - Download forecast CSV files

## 🎯 Usage

1. Start both backend and frontend servers
2. Open the dashboard in your browser
3. Use the configuration panel to set:
   - Train/Test Ratio (60:40, 70:30, or 80:20)
   - Sensitivity Level (Low, Medium, High)
   - Forecast Periods (days)
4. Click "Load Forecast" to generate predictions
5. Click "Load Anomalies" to detect cost anomalies
6. Click "View RCA" on any anomaly to see root cause analysis
7. Use "Security Analysis" to view security insights
8. Generate service-level forecasts to get CSV exports

## 📈 Output Files

Service forecasts are saved in the `outputs/` directory:
- `forecast_service_long.csv` - Long format (date, service, forecast)
- `forecast_service_wide.csv` - Wide format (date as rows, services as columns)

## 🔧 Technologies Used

- **Backend**: Flask, Prophet, Pandas, NumPy, Gunicorn
- **Frontend**: React, Recharts, Axios, React Toastify
- **ML**: Facebook Prophet for time series forecasting
- **Security**: Flask-Limiter (rate limiting), Marshmallow (validation), API key auth, secure headers, audit logging

## 🔐 Security Features

The project includes comprehensive security features:

- ✅ **Rate Limiting** - Protects against API abuse (200/day, 50/hour default)
- ✅ **Input Validation** - All POST endpoints validate input with Marshmallow schemas
- ✅ **API Key Authentication** - Optional in dev, required in production
- ✅ **Secure HTTP Headers** - X-Content-Type-Options, CSP, HSTS, etc.
- ✅ **Audit Logging** - All API requests logged to `backend/logs/audit.log`
- ✅ **Error Handling** - Comprehensive error handlers that don't leak sensitive info
- ✅ **Path Traversal Protection** - Secure file downloads
- ✅ **Environment Variables** - Secrets management via .env files

**See `SECURITY_IMPLEMENTATION_SUMMARY.md` for complete details.**

## 📝 Notes

- The dataset should have columns: UsageDate, ServiceName, Region, ProjectTag, CostINR
- If a units column exists, unit cost computation will use it
- Service-level forecasting uses Prophet when possible, falls back to proportional distribution
- Anomaly detection compares actual costs against Prophet's upper confidence bound

## 🔄 Using a Different Dataset

**See `DATASET_REQUIREMENTS.md` for complete instructions.**

## 🖥️ Cross-Platform Migration

**Moving from Mac to Windows?** See `CROSS_PLATFORM_MIGRATION.md` for complete setup instructions.

**Preparing project for transfer?** See `PREPARE_FOR_TRANSFER.md` for what to include/exclude.

**Quick Guide:**
1. Your CSV must have these columns: `UsageDate`, `ServiceName`, `Region`, `ProjectTag`, `CostINR`
2. Replace `ideal_cost_data.csv` with your file (or rename your file to match)
3. Restart the backend server
4. That's it! The project will work with your new data.

**If your columns have different names:**
- Option 1: Rename your CSV columns to match (easiest)
- Option 2: Update `backend/app.py` to use your column names

