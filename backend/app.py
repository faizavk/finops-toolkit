from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from functools import wraps
# Import rate limiter with fallback
try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    LIMITER_AVAILABLE = True
except (ImportError, Exception) as e:
    LIMITER_AVAILABLE = False
    # Create dummy limiter decorator that does nothing
    class DummyLimiter:
        def __init__(self, *args, **kwargs):
            pass
        def limit(self, *args, **kwargs):
            def decorator(f):
                @wraps(f)
                def wrapper(*args, **kwargs):
                    return f(*args, **kwargs)
                return wrapper
            return decorator
    Limiter = DummyLimiter
    def get_remote_address():
        return '127.0.0.1'
    print(f"Warning: flask-limiter not installed ({e}). Rate limiting disabled.")
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
import logging
from logging.handlers import RotatingFileHandler
from prophet import Prophet
# Import dotenv with fallback
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using system environment variables.")
# Import security modules with fallback for missing dependencies
try:
    from schemas import ForecastRequestSchema, AnomalyRequestSchema, ServiceForecastRequestSchema
    SCHEMAS_AVAILABLE = True
except ImportError:
    SCHEMAS_AVAILABLE = False
    print("Warning: marshmallow not installed. Input validation disabled.")

try:
    from auth import require_api_key, get_api_key_from_request
    AUTH_AVAILABLE = True
except (ImportError, Exception) as e:
    AUTH_AVAILABLE = False
    # Create dummy decorator if auth not available
    def require_api_key(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    def get_api_key_from_request():
        return None
    print(f"Warning: Auth module not available ({e}). API key auth disabled.")
import warnings
warnings.filterwarnings('ignore')

# Environment variables loaded above (if dotenv available)

app = Flask(__name__)

# Configure CORS - Allow from all origins (can be restricted in production)
# In production, replace "*" with your frontend URL
frontend_url = os.getenv('FRONTEND_URL', '*')
#CORS(app, resources={r"/api/*": {"origins": frontend_url if frontend_url != '*' else "*"}})
CORS(app, resources={r"/*": {"origins": "*"}})
# Configure Rate Limiting (if available)
if LIMITER_AVAILABLE:
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
        headers_enabled=True
    )
else:
    # Dummy limiter instance that does nothing
    limiter = Limiter(app=app, key_func=get_remote_address)

# Configure Logging (with fallback if logs directory doesn't exist)
try:
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler('logs/audit.log', maxBytes=10000000, backupCount=5),
            logging.StreamHandler()
        ]
    )
except Exception as e:
    # Fallback: just use console logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    print(f"Warning: Could not set up file logging: {e}")

logger = logging.getLogger(__name__)

# Global variables for model state
current_train_ratio = 0.8
current_sensitivity = 'Medium'
prophet_model = None
historical_data = None
forecast_data = None
anomalies_data = None

# Load data
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ideal_cost_data.csv')

def load_data():
    """Load and preprocess the cost data"""
    global historical_data
    df = pd.read_csv(DATA_FILE)
    df['UsageDate'] = pd.to_datetime(df['UsageDate'])
    df = df.sort_values('UsageDate')
    historical_data = df
    return df

def aggregate_daily_costs(df):
    """Aggregate costs by date"""
    daily = df.groupby('UsageDate')['CostINR'].sum().reset_index()
    daily.columns = ['ds', 'y']
    return daily

def train_prophet_model(train_ratio=0.8, periods=30):
    """Train Prophet model with specified train/test ratio"""
    global prophet_model, forecast_data
    
    df = load_data()
    daily = aggregate_daily_costs(df)
    
    # Split data
    split_idx = int(len(daily) * train_ratio)
    train_data = daily.iloc[:split_idx].copy()
    
    # Try to train Prophet, with fallback to simple forecasting
    try:
        # Train Prophet
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            interval_width=0.95
        )
        model.fit(train_data)
        
        # Generate forecast
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        prophet_model = model
        forecast_data = forecast
        
        return {
            'train_data': train_data.to_dict('records'),
            'forecast': forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records'),
            'historical': daily.to_dict('records')
        }
    except Exception as e:
        # Fallback: Simple moving average forecast
        print(f"Prophet failed: {e}. Using fallback method.")
        last_date = train_data['ds'].max()
        last_value = train_data['y'].iloc[-1]
        mean_value = train_data['y'].mean()
        std_value = train_data['y'].std()
        
        # Generate simple forecast
        forecast_list = []
        for i in range(1, periods + 1):
            future_date = last_date + timedelta(days=i)
            # Simple trend: use recent average with some variation
            forecast_value = mean_value
            forecast_list.append({
                'ds': future_date,
                'yhat': forecast_value,
                'yhat_lower': max(0, forecast_value - 1.96 * std_value),
                'yhat_upper': forecast_value + 1.96 * std_value
            })
        
        # Combine historical with forecast
        historical_forecast_df = pd.DataFrame([{
            'ds': row['ds'], 
            'yhat': row['y'], 
            'yhat_lower': row['y'], 
            'yhat_upper': row['y']
        } for _, row in train_data.iterrows()])
        
        future_forecast_df = pd.DataFrame(forecast_list)
        all_forecast = pd.concat([historical_forecast_df, future_forecast_df], ignore_index=True)
        
        forecast_data = all_forecast
        
        return {
            'train_data': train_data.to_dict('records'),
            'forecast': forecast_list,
            'historical': daily.to_dict('records')
        }

def detect_anomalies(sensitivity='Medium', periods=30):
    """Detect anomalies based on Prophet forecast and sensitivity"""
    global prophet_model, historical_data, forecast_data
    
    if prophet_model is None or forecast_data is None:
        train_prophet_model(current_train_ratio, periods)
    
    df = load_data()
    daily = aggregate_daily_costs(df)
    
    # Get historical predictions
    try:
        if prophet_model is not None:
            historical_forecast = prophet_model.predict(
                prophet_model.make_future_dataframe(periods=0)
            )
        else:
            # Use forecast_data if available, otherwise create simple predictions
            if forecast_data is not None:
                historical_forecast = forecast_data[forecast_data['ds'] <= daily['ds'].max()].copy()
            else:
                # Fallback: use mean and std
                mean_val = daily['y'].mean()
                std_val = daily['y'].std()
                historical_forecast = daily.copy()
                historical_forecast['yhat'] = mean_val
                historical_forecast['yhat_upper'] = mean_val + 1.96 * std_val
                historical_forecast['yhat_lower'] = max(0, mean_val - 1.96 * std_val)
    except Exception as e:
        # Fallback method
        mean_val = daily['y'].mean()
        std_val = daily['y'].std()
        historical_forecast = daily.copy()
        historical_forecast['yhat'] = mean_val
        historical_forecast['yhat_upper'] = mean_val + 1.96 * std_val
        historical_forecast['yhat_lower'] = max(0, mean_val - 1.96 * std_val)
    
    # Merge actual with predictions
    merged = daily.merge(
        historical_forecast[['ds', 'yhat', 'yhat_upper', 'yhat_lower']],
        on='ds',
        how='left'
    )
    
    # Sensitivity multipliers
    sensitivity_multipliers = {
        'Low': 1.5,
        'Medium': 1.2,
        'High': 1.0
    }
    
    threshold = sensitivity_multipliers.get(sensitivity, 1.2)
    
    # Detect anomalies
    merged['is_anomaly'] = merged['y'] > (merged['yhat_upper'] * threshold)
    anomalies = merged[merged['is_anomaly']].copy()
    
    anomalies_list = []
    for _, row in anomalies.iterrows():
        date = row['ds']
        actual = row['y']
        predicted = row['yhat']
        upper = row['yhat_upper']
        
        # Get RCA data for this date
        date_data = historical_data[historical_data['UsageDate'] == date]
        
        # Top services
        top_services = date_data.groupby('ServiceName')['CostINR'].sum().sort_values(ascending=False).head(5)
        
        # Top regions
        top_regions = date_data.groupby('Region')['CostINR'].sum().sort_values(ascending=False).head(5)
        
        # Top tags
        top_tags = date_data.groupby('ProjectTag')['CostINR'].sum().sort_values(ascending=False).head(5)
        
        anomalies_list.append({
            'date': date.strftime('%Y-%m-%d'),
            'actual_cost': float(actual),
            'predicted_cost': float(predicted),
            'upper_bound': float(upper),
            'deviation': float(actual - predicted),
            'deviation_percent': float((actual - predicted) / predicted * 100) if predicted > 0 else 0,
            'rca': {
                'top_services': top_services.to_dict(),
                'top_regions': top_regions.to_dict(),
                'top_tags': top_tags.to_dict()
            }
        })
    
    global anomalies_data
    anomalies_data = anomalies_list
    
    return anomalies_list

def compute_unit_costs():
    """Compute unit costs if units column exists, otherwise compute per service/region"""
    df = load_data()
    
    # Since there's no units column, compute cost per service/region/tag
    unit_costs = []
    
    # Service-level unit costs (cost per service occurrence)
    service_counts = df.groupby(['UsageDate', 'ServiceName']).size().reset_index(name='count')
    service_costs = df.groupby(['UsageDate', 'ServiceName'])['CostINR'].sum().reset_index()
    service_unit = service_costs.merge(service_counts, on=['UsageDate', 'ServiceName'])
    service_unit['unit_cost'] = service_unit['CostINR'] / service_unit['count']
    
    # Region-level
    region_counts = df.groupby(['UsageDate', 'Region']).size().reset_index(name='count')
    region_costs = df.groupby(['UsageDate', 'Region'])['CostINR'].sum().reset_index()
    region_unit = region_costs.merge(region_counts, on=['UsageDate', 'Region'])
    region_unit['unit_cost'] = region_unit['CostINR'] / region_unit['count']
    
    # Tag-level
    tag_counts = df.groupby(['UsageDate', 'ProjectTag']).size().reset_index(name='count')
    tag_costs = df.groupby(['UsageDate', 'ProjectTag'])['CostINR'].sum().reset_index()
    tag_unit = tag_costs.merge(tag_counts, on=['UsageDate', 'ProjectTag'])
    tag_unit['unit_cost'] = tag_unit['CostINR'] / tag_unit['count']
    
    return {
        'service_unit_costs': service_unit.to_dict('records'),
        'region_unit_costs': region_unit.to_dict('records'),
        'tag_unit_costs': tag_unit.to_dict('records'),
        'average_unit_cost': float(df['CostINR'].sum() / len(df))
    }

def get_security_insights():
    """Get security insights: extreme spikes and rare tags"""
    global prophet_model, historical_data, forecast_data
    
    if prophet_model is None or forecast_data is None:
        train_prophet_model(current_train_ratio, 30)
    
    df = load_data()
    daily = aggregate_daily_costs(df)
    
    # Get predictions
    try:
        if prophet_model is not None:
            historical_forecast = prophet_model.predict(
                prophet_model.make_future_dataframe(periods=0)
            )
        else:
            # Use forecast_data or fallback
            if forecast_data is not None:
                historical_forecast = forecast_data[forecast_data['ds'] <= daily['ds'].max()].copy()
            else:
                mean_val = daily['y'].mean()
                historical_forecast = daily.copy()
                historical_forecast['yhat'] = mean_val
    except Exception as e:
        # Fallback method
        mean_val = daily['y'].mean()
        historical_forecast = daily.copy()
        historical_forecast['yhat'] = mean_val
    
    merged = daily.merge(
        historical_forecast[['ds', 'yhat']],
        on='ds',
        how='left'
    )
    
    # Extreme spikes (actual > 10x predicted)
    merged['spike_ratio'] = merged['y'] / merged['yhat']
    extreme_spikes = merged[merged['spike_ratio'] > 10].copy()
    
    # Rare or new tags
    all_tags = set(df['ProjectTag'].unique())
    recent_dates = df['UsageDate'].max() - timedelta(days=30)
    recent_tags = set(df[df['UsageDate'] >= recent_dates]['ProjectTag'].unique())
    old_tags = set(df[df['UsageDate'] < recent_dates]['ProjectTag'].unique())
    
    # Tags that appeared recently but not before (new tags)
    new_tags = recent_tags - old_tags
    
    # Tags that appeared before but not recently (rare/disappeared tags)
    rare_tags = old_tags - recent_tags
    
    # Tag frequency analysis
    tag_freq = df.groupby('ProjectTag').size()
    rare_tags_by_freq = tag_freq[tag_freq < tag_freq.quantile(0.1)].index.tolist()
    
    return {
        'extreme_spikes': extreme_spikes[['ds', 'y', 'yhat', 'spike_ratio']].to_dict('records'),
        'rare_tags': list(rare_tags),
        'rare_tags_by_frequency': rare_tags_by_freq,
        'new_tags': list(new_tags)
    }

def forecast_by_service(periods=30):
    """Forecast costs by service using Prophet or proportional distribution"""
    global prophet_model, forecast_data, historical_data
    
    if prophet_model is None or forecast_data is None:
        train_prophet_model(current_train_ratio, periods)
    
    df = load_data()
    # Diagnostic logging for troubleshooting empty service forecasts
    try:
        logger.info(f"forecast_by_service: loaded df shape={df.shape}, columns={list(df.columns)}")
    except Exception:
        logger.info("forecast_by_service: loaded df (unable to stringify shape)")

    #services = df['ServiceName'].unique()
    
    # Get total forecast (future dates only)
    #last_date = historical_data['UsageDate'].max()
    if df.empty:
        logger.error("Cannot generate service forecast: historical data is empty.")
        return {'error': 'No historical data available', 'long': [], 'wide':[]}
    
    if historical_data is None or historical_data.empty:
        historical_data = df

    services = df['ServiceName'].unique()
    last_date = df['UsageDate'].max()

    try:
        logger.info(f"forecast_by_service: unique services count={len(services)}; sample_services={list(services)[:10]}")
    except Exception:
        logger.info("forecast_by_service: could not log services list")

    mean_val = df.groupby('UsageDate')['CostINR'].sum().mean()
    
    if forecast_data is not None and not forecast_data.empty:
        # Filter for future dates only
        if 'ds' in forecast_data.columns:
            # Convert to datetime if needed
            if not pd.api.types.is_datetime64_any_dtype(forecast_data['ds']):
                forecast_data['ds'] = pd.to_datetime(forecast_data['ds'])
            # Ensure last_date is datetime
            if not isinstance(last_date, pd.Timestamp):
                last_date = pd.to_datetime(last_date)
            total_forecast = forecast_data[forecast_data['ds'] > last_date].copy()
            
            # If filtering resulted in empty, create forecast manually
            if total_forecast.empty:
                total_forecast = pd.DataFrame([{
                    'ds': last_date + timedelta(days=i+1),
                    'yhat': mean_val,
                    'yhat_lower': mean_val * 0.9,
                    'yhat_upper': mean_val * 1.1
                } for i in range(periods)])
        else:
            # If forecast_data doesn't have 'ds', create it
            total_forecast = pd.DataFrame([{
                'ds': last_date + timedelta(days=i+1),
                'yhat': mean_val,
                'yhat_lower': mean_val * 0.9,
                'yhat_upper': mean_val * 1.1
            } for i in range(periods)])
    else:
        # Create simple forecast if needed
        total_forecast = pd.DataFrame([{
            'ds': last_date + timedelta(days=i+1),
            'yhat': mean_val,
            'yhat_lower': mean_val * 0.9,
            'yhat_upper': mean_val * 1.1
        } for i in range(periods)])
    
    # Ensure total_forecast is not empty and has required columns
    if total_forecast.empty or 'yhat' not in total_forecast.columns:
        total_forecast = pd.DataFrame([{
            'ds': last_date + timedelta(days=i+1),
            'yhat': mean_val,
            'yhat_lower': mean_val * 0.9,
            'yhat_upper': mean_val * 1.1
        } for i in range(periods)])
    
    service_forecasts = {}
    service_forecasts_long = []
   
    logger.info(f"Service forecast: Found {len(services)} services, total_forecast has {len(total_forecast)} rows")
   
    # Ensure total_forecast has datetime column
    if not total_forecast.empty and 'ds' in total_forecast.columns:
        if not pd.api.types.is_datetime64_any_dtype(total_forecast['ds']):
            total_forecast['ds'] = pd.to_datetime(total_forecast['ds'])
   
    for service in services:
        logger.info(f"Processing service: {service}")
        service_data = df[df['ServiceName'] == service]
        service_daily = service_data.groupby('UsageDate')['CostINR'].sum().reset_index()
        service_daily.columns = ['ds', 'y']
        try:
            logger.info(f"  service_daily rows: {len(service_daily)}; service_data rows: {len(service_data)}")
        except Exception:
            logger.info("  service_daily info unavailable")
        '''
        if len(service_daily) < 7:  # Not enough data for Prophet
            # Use proportional distribution
            historical_service_total = service_data['CostINR'].sum()
            historical_total = df['CostINR'].sum()
            proportion = historical_service_total / historical_total if historical_total > 0 else 0
        '''
        if len(service_daily) < 7:  # Not enough data for Prophet
            # Use proportional distribution
            historical_service_total = service_data['CostINR'].sum()
            historical_total = df['CostINR'].sum()
            proportion = historical_service_total / historical_total if historical_total > 0 else 0
            
            logger.info(f"  Using proportional distribution - proportion: {proportion}, total_forecast rows: {len(total_forecast)}")
            
            if total_forecast.empty:
                logger.error(f"  ERROR: total_forecast is empty for service {service}!")
                continue
            first_appended = False
            for idx, row in total_forecast.iterrows():
                try:
                    date_str = row['ds'].strftime('%Y-%m-%d') if hasattr(row['ds'], 'strftime') else str(row['ds'])[:10]
                    service_forecasts_long.append({
                        'date': date_str,
                        'service': str(service),  # Ensure it's a string
                        'forecast': float(row['yhat'] * proportion),
                        'forecast_lower': float(row['yhat_lower'] * proportion),
                        'forecast_upper': float(row['yhat_upper'] * proportion)
                    })
                except Exception as e:
                    logger.error(f"  Error adding forecast row for {service}: {e}")
                    continue
                if not first_appended:
                    logger.info(f"  Appended first proportional forecast row for service: {service}")
                    first_appended = True
        else:
            # Try Prophet
            try:
                if prophet_model is not None:  # Only try Prophet if main model works
                    # Train on the full service history so future predictions extend beyond
                    # the latest historical date. Training only on the train split can
                    # result in forecasts that don't reach past the full history when
                    # the withheld portion is larger than `periods`.
                    train_service = service_daily.copy()

                    service_model = Prophet(
                        yearly_seasonality=False,
                        weekly_seasonality=True,
                        daily_seasonality=False,
                        interval_width=0.95
                    )
                    service_model.fit(train_service)
                    
                    service_future = service_model.make_future_dataframe(periods=periods)
                    service_forecast = service_model.predict(service_future)
                    
                    # Select only future rows beyond the known historical max date
                    future_service_forecast = service_forecast[service_forecast['ds'] > service_daily['ds'].max()]
                    
                    for _, row in future_service_forecast.iterrows():
                        service_forecasts_long.append({
                            'date': row['ds'].strftime('%Y-%m-%d'),
                            'service': service,
                            'forecast': float(row['yhat']),
                            'forecast_lower': float(row['yhat_lower']),
                            'forecast_upper': float(row['yhat_upper'])
                        })
                    if len(future_service_forecast) > 0:
                        logger.info(f"  Appended {len(future_service_forecast)} prophet forecast rows for service: {service}")
                else:
                    raise Exception("Prophet not available")
            except:
                # Fallback to proportional
                historical_service_total = service_data['CostINR'].sum()
                historical_total = df['CostINR'].sum()
                proportion = historical_service_total / historical_total if historical_total > 0 else 0
                
                for _, row in total_forecast.iterrows():
                    service_forecasts_long.append({
                        'date': row['ds'].strftime('%Y-%m-%d'),
                        'service': service,
                        'forecast': float(row['yhat'] * proportion),
                        'forecast_lower': float(row['yhat_lower'] * proportion),
                        'forecast_upper': float(row['yhat_upper'] * proportion)
                    })
    logger.info(f"After loop: service_forecasts_long has {len(service_forecasts_long)} entries")
    # Create wide format
    service_forecasts_wide = pd.DataFrame(service_forecasts_long)
    if not service_forecasts_wide.empty:
        service_forecasts_wide = service_forecasts_wide.pivot_table(
            index='date',
            columns='service',
            values='forecast',
            aggfunc='sum'
        ).reset_index()
        service_forecasts_wide = service_forecasts_wide.fillna(0)
    
    return {
        'long': service_forecasts_long,
        'wide': service_forecasts_wide.to_dict('records') if not service_forecasts_wide.empty else []
    }

# Security: Add secure headers to all responses
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

# Security: Log all API requests
@app.before_request
def log_request():
    """Log API access for audit trail"""
    if request.path.startswith('/api/'):
        api_key = get_api_key_from_request()
        user = api_key[:10] + '...' if api_key else 'anonymous'
        logger.info(
            f"API Request - {request.method} {request.path} - "
            f"User: {user} - IP: {request.remote_addr}"
        )

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 Error - {request.path} - IP: {request.remote_addr}")
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 Error - {request.path} - IP: {request.remote_addr} - Error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit errors"""
    logger.warning(f"Rate limit exceeded - IP: {request.remote_addr}")
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': 'Too many requests. Please try again later.',
        'retry_after': str(e.description) if hasattr(e, 'description') else None
    }), 429

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    logger.warning(f"400 Error - {request.path} - IP: {request.remote_addr}")
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

# API Routes

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint - No authentication required"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/historical', methods=['GET'])
@limiter.limit("30 per minute")
@require_api_key
def get_historical():
    """Feature 1: Historical Cost Visualization"""
    try:
        df = load_data()
        daily = aggregate_daily_costs(df)
        logger.info(f"Historical data requested - Records: {len(daily)}")
        return jsonify(daily.to_dict('records'))
    except Exception as e:
        logger.error(f"Error in get_historical: {str(e)}")
        return jsonify({'error': 'Failed to load historical data'}), 500

@app.route('/api/forecast', methods=['POST'])
@limiter.limit("10 per minute")
@require_api_key
def get_forecast():
    """Feature 2: Future Forecasting with Prophet"""
    try:
        # Validate input (if schemas available)
        if SCHEMAS_AVAILABLE:
            schema = ForecastRequestSchema()
            try:
                data = schema.load(request.json or {})
            except Exception as e:
                logger.warning(f"Invalid forecast request - {str(e)} - IP: {request.remote_addr}")
                return jsonify({'error': 'Invalid request data', 'details': str(e)}), 400
        else:
            # Fallback: basic validation
            data = request.json or {}
            if 'train_ratio' in data and (data['train_ratio'] < 0.1 or data['train_ratio'] > 0.9):
                return jsonify({'error': 'train_ratio must be between 0.1 and 0.9'}), 400
        
        train_ratio = data.get('train_ratio', 0.8)
        periods = data.get('periods', 30)
        sensitivity = data.get('sensitivity', 'Medium')
        
        global current_train_ratio, current_sensitivity
        current_train_ratio = train_ratio
        current_sensitivity = sensitivity
        
        logger.info(f"Forecast requested - Ratio: {train_ratio}, Periods: {periods}, Sensitivity: {sensitivity}")
        result = train_prophet_model(train_ratio, periods)
        logger.info(f"Forecast generated successfully - Records: {len(result.get('forecast', []))}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in get_forecast: {str(e)}")
        return jsonify({'error': 'Failed to generate forecast', 'message': str(e)}), 500

@app.route('/api/anomalies', methods=['POST'])
@limiter.limit("10 per minute")
@require_api_key
def get_anomalies():
    """Feature 5: Anomaly Detection"""
    try:
        # Validate input (if schemas available)
        if SCHEMAS_AVAILABLE:
            schema = AnomalyRequestSchema()
            try:
                data = schema.load(request.json or {})
            except Exception as e:
                logger.warning(f"Invalid anomaly request - {str(e)} - IP: {request.remote_addr}")
                return jsonify({'error': 'Invalid request data', 'details': str(e)}), 400
        else:
            data = request.json or {}
        
        sensitivity = data.get('sensitivity', 'Medium')
        periods = data.get('periods', 30)
        
        global current_sensitivity
        current_sensitivity = sensitivity
        
        logger.info(f"Anomaly detection requested - Sensitivity: {sensitivity}, Periods: {periods}")
        anomalies = detect_anomalies(sensitivity, periods)
        logger.info(f"Anomalies detected - Count: {len(anomalies)}")
        return jsonify(anomalies)
    except Exception as e:
        logger.error(f"Error in get_anomalies: {str(e)}")
        return jsonify({'error': 'Failed to detect anomalies', 'message': str(e)}), 500

@app.route('/api/rca/<date>', methods=['GET'])
@limiter.limit("30 per minute")
@require_api_key
def get_rca(date):
    """Feature 6: Root Cause Analysis"""
    try:
        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            logger.warning(f"Invalid date format in RCA request - {date} - IP: {request.remote_addr}")
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        logger.info(f"RCA requested for date: {date}")
        anomalies = detect_anomalies(current_sensitivity, 30)
        for anomaly in anomalies:
            if anomaly['date'] == date:
                logger.info(f"RCA found for date: {date}")
                return jsonify(anomaly['rca'])
        
        logger.warning(f"RCA not found for date: {date}")
        return jsonify({'error': 'Anomaly not found for this date'}), 404
    except Exception as e:
        logger.error(f"Error in get_rca: {str(e)}")
        return jsonify({'error': 'Failed to get RCA', 'message': str(e)}), 500

@app.route('/api/unit-costs', methods=['GET'])
@limiter.limit("30 per minute")
@require_api_key
def get_unit_costs():
    """Feature 7: Unit Cost Computation"""
    try:
        logger.info("Unit costs computation requested")
        unit_costs = compute_unit_costs()
        return jsonify(unit_costs)
    except Exception as e:
        logger.error(f"Error in get_unit_costs: {str(e)}")
        return jsonify({'error': 'Failed to compute unit costs', 'message': str(e)}), 500

@app.route('/api/security', methods=['GET'])
@limiter.limit("20 per minute")
@require_api_key
def get_security():
    """Feature 8: Security Insights"""
    try:
        logger.info("Security insights requested")
        insights = get_security_insights()
        return jsonify(insights)
    except Exception as e:
        logger.error(f"Error in get_security: {str(e)}")
        return jsonify({'error': 'Failed to get security insights', 'message': str(e)}), 500

@app.route('/api/service-forecast', methods=['POST'])
@limiter.limit("5 per minute")  # More restrictive as this is resource-intensive
@require_api_key
def get_service_forecast():
    """Feature 9: Service-Level Forecast"""
    try:
        # Validate input (if schemas available)
        if SCHEMAS_AVAILABLE:
            schema = ServiceForecastRequestSchema()
            try:
                data = schema.load(request.json or {})
            except Exception as e:
                logger.warning(f"Invalid service forecast request - {str(e)} - IP: {request.remote_addr}")
                return jsonify({'error': 'Invalid request data', 'details': str(e)}), 400
        else:
            data = request.json or {}
        
        periods = data.get('periods', 30)
        
        logger.info(f"Service forecast requested - Periods: {periods}")
        forecasts = forecast_by_service(periods)
        
        # Save to CSV files
        long_df = pd.DataFrame(forecasts['long'])
        wide_df = pd.DataFrame(forecasts['wide'])
        
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        
        long_df.to_csv(os.path.join(output_dir, 'forecast_service_long.csv'), index=False)
        if not wide_df.empty:
            wide_df.to_csv(os.path.join(output_dir, 'forecast_service_wide.csv'), index=False)
        
        logger.info(f"Service forecast generated - Services: {len(set([f['service'] for f in forecasts['long']]))}")
        return jsonify(forecasts)
    except Exception as e:
        logger.error(f"Error in get_service_forecast: {str(e)}")
        return jsonify({'error': 'Failed to generate service forecast', 'message': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
@limiter.limit("20 per minute")
@require_api_key
def download_file(filename):
    """Download forecast CSV files"""
    try:
        # Security: Validate filename to prevent path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            logger.warning(f"Path traversal attempt - Filename: {filename} - IP: {request.remote_addr}")
            return jsonify({'error': 'Invalid filename'}), 400
        
        # Only allow specific files
        allowed_files = ['forecast_service_long.csv', 'forecast_service_wide.csv']
        if filename not in allowed_files:
            logger.warning(f"Unauthorized file download attempt - Filename: {filename} - IP: {request.remote_addr}")
            return jsonify({'error': 'File not allowed'}), 403
        
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
        file_path = os.path.join(output_dir, filename)
        
        if os.path.exists(file_path):
            logger.info(f"File download - Filename: {filename}")
            return send_file(file_path, as_attachment=True)
        
        logger.warning(f"File not found - Filename: {filename}")
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error in download_file: {str(e)}")
        return jsonify({'error': 'Failed to download file', 'message': str(e)}), 500

if __name__ == '__main__':
    # Initialize data
    load_data()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

