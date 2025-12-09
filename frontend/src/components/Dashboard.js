import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import './Dashboard.css';
import CostChart from './CostChart';
import ForecastChart from './ForecastChart';
import AnomaliesTable from './AnomaliesTable';
import RCAModal from './RCAModal';
import SecurityInsights from './SecurityInsights';
import ServiceForecastChart from './ServiceForecastChart';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
const API_KEY = process.env.REACT_APP_API_KEY || ''; // Optional API key for production

function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [historicalData, setHistoricalData] = useState([]);
  const [forecastData, setForecastData] = useState(null);
  const [anomalies, setAnomalies] = useState([]);
  const [securityInsights, setSecurityInsights] = useState(null);
  const [unitCosts, setUnitCosts] = useState(null);
  const [serviceForecast, setServiceForecast] = useState(null);
  const [selectedAnomaly, setSelectedAnomaly] = useState(null);
  const [showRCAModal, setShowRCAModal] = useState(false);
  
  // Configuration
  const [trainRatio, setTrainRatio] = useState(0.8);
  const [sensitivity, setSensitivity] = useState('Medium');
  const [forecastPeriods, setForecastPeriods] = useState(30);

  useEffect(() => {
    loadHistoricalData();
  }, []);

  // Helper function to make API calls with security headers
  const apiCall = async (method, url, data = null) => {
    const config = {
      method,
      url: `${API_BASE}${url}`,
      headers: {
        'Content-Type': 'application/json',
      },
    };
    
    // Add API key if provided
    if (API_KEY) {
      config.headers['X-API-Key'] = API_KEY;
    }
    
    // Add data for POST requests
    if (data) {
      config.data = data;
    }
    
    return axios(config);
  };

  const loadHistoricalData = async () => {
    try {
      setLoading(true);
      const response = await apiCall('get', '/historical');
      setHistoricalData(response.data);
      toast.success('Historical data loaded');
    } catch (error) {
      let errorMsg = 'Failed to load historical data';
      if (error.response) {
        // Server responded with error
        if (error.response.status === 401) {
          errorMsg = 'Authentication required. Please check API key.';
        } else if (error.response.status === 429) {
          errorMsg = 'Rate limit exceeded. Please try again later.';
        } else if (error.response.data?.error) {
          errorMsg = `Error: ${error.response.data.error}`;
        } else {
          errorMsg = `Server error (${error.response.status}): ${error.response.statusText}`;
        }
      } else if (error.request) {
        // Request made but no response
        errorMsg = 'Cannot connect to backend. Is the server running on http://localhost:5000?';
      } else {
        // Error setting up request
        errorMsg = `Request error: ${error.message}`;
      }
      toast.error(errorMsg);
      console.error('Historical data error:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadForecast = async () => {
    try {
      setLoading(true);
      const response = await apiCall('post', '/forecast', {
        train_ratio: trainRatio,
        periods: forecastPeriods,
        sensitivity: sensitivity
      });
      setForecastData(response.data);
      toast.success('Forecast generated successfully');
    } catch (error) {
      let errorMsg = 'Failed to generate forecast';
      if (error.response) {
        if (error.response.status === 401) {
          errorMsg = 'Authentication required. Please check API key.';
        } else if (error.response.status === 400) {
          errorMsg = `Invalid request: ${error.response.data?.error || 'Check your input'}`;
        } else if (error.response.status === 429) {
          errorMsg = 'Rate limit exceeded. Please try again later.';
        } else if (error.response.data?.error) {
          errorMsg = `Error: ${error.response.data.error}`;
        } else {
          errorMsg = `Server error (${error.response.status}): ${error.response.statusText}`;
        }
      } else if (error.request) {
        errorMsg = 'Cannot connect to backend. Is the server running on http://localhost:5000?';
      } else {
        errorMsg = `Request error: ${error.message}`;
      }
      toast.error(errorMsg);
      console.error('Forecast error:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadAnomalies = async () => {
    try {
      setLoading(true);
      const response = await apiCall('post', '/anomalies', {
        sensitivity: sensitivity,
        periods: forecastPeriods
      });
      setAnomalies(response.data);
      toast.success(`Found ${response.data.length} anomalies`);
    } catch (error) {
      let errorMsg = 'Failed to detect anomalies';
      if (error.response) {
        if (error.response.status === 401) {
          errorMsg = 'Authentication required. Please check API key.';
        } else if (error.response.status === 400) {
          errorMsg = `Invalid request: ${error.response.data?.error || 'Check your input'}`;
        } else if (error.response.status === 429) {
          errorMsg = 'Rate limit exceeded. Please try again later.';
        } else if (error.response.data?.error) {
          errorMsg = `Error: ${error.response.data.error}`;
        } else {
          errorMsg = `Server error (${error.response.status}): ${error.response.statusText}`;
        }
      } else if (error.request) {
        errorMsg = 'Cannot connect to backend. Is the server running on http://localhost:5000?';
      } else {
        errorMsg = `Request error: ${error.message}`;
      }
      toast.error(errorMsg);
      console.error('Anomalies error:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadSecurityInsights = async () => {
    try {
      setLoading(true);
      const response = await apiCall('get', '/security');
      setSecurityInsights(response.data);
      toast.success('Security insights loaded');
    } catch (error) {
      let errorMsg = 'Failed to load security insights';
      if (error.response) {
        if (error.response.status === 401) {
          errorMsg = 'Authentication required. Please check API key.';
        } else if (error.response.status === 429) {
          errorMsg = 'Rate limit exceeded. Please try again later.';
        } else if (error.response.data?.error) {
          errorMsg = `Error: ${error.response.data.error}`;
        } else {
          errorMsg = `Server error (${error.response.status}): ${error.response.statusText}`;
        }
      } else if (error.request) {
        errorMsg = 'Cannot connect to backend. Is the server running on http://localhost:5000?';
      } else {
        errorMsg = `Request error: ${error.message}`;
      }
      toast.error(errorMsg);
      console.error('Security insights error:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadUnitCosts = async () => {
    try {
      setLoading(true);
      const response = await apiCall('get', '/unit-costs');
      setUnitCosts(response.data);
      toast.success('Unit costs computed');
    } catch (error) {
      let errorMsg = 'Failed to compute unit costs';
      if (error.response) {
        if (error.response.status === 401) {
          errorMsg = 'Authentication required. Please check API key.';
        } else if (error.response.status === 429) {
          errorMsg = 'Rate limit exceeded. Please try again later.';
        } else if (error.response.data?.error) {
          errorMsg = `Error: ${error.response.data.error}`;
        } else {
          errorMsg = `Server error (${error.response.status}): ${error.response.statusText}`;
        }
      } else if (error.request) {
        errorMsg = 'Cannot connect to backend. Is the server running on http://localhost:5000?';
      } else {
        errorMsg = `Request error: ${error.message}`;
      }
      toast.error(errorMsg);
      console.error('Unit costs error:', error);
    } finally {
      setLoading(false);
    }
  };

  const retrainModel = async () => {
    try {
      setLoading(true);
      await loadForecast();
      await loadAnomalies();
      toast.success('Model retrained with new parameters');
    } catch (error) {
      toast.error('Failed to retrain model');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const generateServiceForecast = async () => {
    try {
      setLoading(true);
      const response = await apiCall('post', '/service-forecast', {
        periods: forecastPeriods
      });
      setServiceForecast(response.data);
      const serviceCount = response.data.long && response.data.long.length > 0 
        ? new Set(response.data.long.map(item => item.service)).size 
        : 0;
      if (serviceCount > 0) {
        toast.success(`Service-level forecast generated for ${serviceCount} services`);
      } else {
        toast.warning('Service forecast generated but no services found');
      }
    } catch (error) {
      let errorMsg = 'Failed to generate service forecast';
      if (error.response) {
        if (error.response.status === 401) {
          errorMsg = 'Authentication required. Please check API key.';
        } else if (error.response.status === 400) {
          errorMsg = `Invalid request: ${error.response.data?.error || 'Check your input'}`;
        } else if (error.response.status === 429) {
          errorMsg = 'Rate limit exceeded. Please try again later.';
        } else if (error.response.data?.error) {
          errorMsg = `Error: ${error.response.data.error}`;
        } else {
          errorMsg = `Server error (${error.response.status}): ${error.response.statusText}`;
        }
      } else if (error.request) {
        errorMsg = 'Cannot connect to backend. Is the server running on http://localhost:5000?';
      } else {
        errorMsg = `Request error: ${error.message}`;
      }
      toast.error(errorMsg);
      console.error('Service forecast error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnomalyClick = (anomaly) => {
    setSelectedAnomaly(anomaly);
    setShowRCAModal(true);
  };

  return (
    <div className="dashboard">
      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      )}

      <header className="dashboard-header">
        <h1>🟦 FinOps Toolkit</h1>
        <p>Cloud Cost Management & Forecasting Dashboard</p>
      </header>

      <div className="dashboard-content">
        {/* Configuration Panel */}
        <div className="config-panel">
          <h2>Configuration</h2>
          
          <div className="config-group">
            <label>Train/Test Ratio:</label>
            <select 
              value={trainRatio} 
              onChange={(e) => setTrainRatio(parseFloat(e.target.value))}
            >
              <option value={0.6}>60:40</option>
              <option value={0.7}>70:30</option>
              <option value={0.8}>80:20</option>
            </select>
          </div>

          <div className="config-group">
            <label>Sensitivity:</label>
            <select 
              value={sensitivity} 
              onChange={(e) => setSensitivity(e.target.value)}
            >
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </div>

          <div className="config-group">
            <label>Forecast Periods (days):</label>
            <input 
              type="number" 
              value={forecastPeriods} 
              onChange={(e) => setForecastPeriods(parseInt(e.target.value))}
              min="1"
              max="365"
            />
          </div>

          <div className="action-buttons">
            <button onClick={loadForecast} className="btn btn-primary">
              Load Forecast
            </button>
            <button onClick={loadAnomalies} className="btn btn-secondary">
              Load Anomalies
            </button>
            <button onClick={retrainModel} className="btn btn-success">
              Retrain Model
            </button>
            <button onClick={loadSecurityInsights} className="btn btn-info">
              Security Analysis
            </button>
            <button onClick={loadUnitCosts} className="btn btn-warning">
              Unit Costs
            </button>
            <button onClick={generateServiceForecast} className="btn btn-purple">
              Service Forecast
            </button>
          </div>
        </div>

        {/* Feature 1: Historical Cost Visualization */}
        <div className="chart-section">
          <h2>Historical Cost Visualization</h2>
          <CostChart data={historicalData} />
        </div>

        {/* Feature 2: Future Forecasting */}
        {forecastData && (
          <div className="chart-section">
            <h2>Future Forecasting with Prophet</h2>
            <ForecastChart 
              historical={forecastData.historical}
              forecast={forecastData.forecast}
            />
          </div>
        )}

        {/* Feature 9: Service-Level Forecast */}
        {serviceForecast && (
          <div className="chart-section">
            <h2>Service-Level Forecast</h2>
            <ServiceForecastChart data={serviceForecast} />
          </div>
        )}

        {/* Feature 5: Anomaly Detection */}
        {anomalies.length > 0 && (
          <div className="anomalies-section">
            <h2>Anomaly Detection ({anomalies.length} found)</h2>
            <AnomaliesTable 
              anomalies={anomalies} 
              onAnomalyClick={handleAnomalyClick}
            />
          </div>
        )}

        {/* Feature 8: Security Insights */}
        {securityInsights && (
          <div className="security-section">
            <h2>Security Insights</h2>
            <SecurityInsights insights={securityInsights} />
          </div>
        )}

        {/* Feature 7: Unit Costs */}
        {unitCosts && (
          <div className="unit-costs-section">
            <h2>Unit Cost Computation</h2>
            <div className="unit-costs-display">
              <p><strong>Average Unit Cost:</strong> ₹{unitCosts.average_unit_cost.toFixed(2)}</p>
              <p><strong>Service Unit Costs:</strong> {unitCosts.service_unit_costs.length} records</p>
              <p><strong>Region Unit Costs:</strong> {unitCosts.region_unit_costs.length} records</p>
              <p><strong>Tag Unit Costs:</strong> {unitCosts.tag_unit_costs.length} records</p>
            </div>
          </div>
        )}
      </div>

      {/* Feature 6: RCA Modal */}
      {showRCAModal && selectedAnomaly && (
        <RCAModal
          anomaly={selectedAnomaly}
          onClose={() => {
            setShowRCAModal(false);
            setSelectedAnomaly(null);
          }}
        />
      )}
    </div>
  );
}

export default Dashboard;

