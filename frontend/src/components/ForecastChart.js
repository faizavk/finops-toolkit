import React from 'react';
import {
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  defs,
  linearGradient,
  stop
} from 'recharts';
import './ForecastChart.css';

function ForecastChart({ historical, forecast }) {
  if (!historical || !forecast) {
    return <div className="no-data">No forecast data available</div>;
  }

  // Combine historical and forecast data
  // UPDATED: Added year: 'numeric'
  const historicalData = historical.map(item => ({
    date: new Date(item.ds).toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    }),
    actual: parseFloat(item.y),
    type: 'historical'
  }));

  // UPDATED: Added year: 'numeric'
  const forecastData = forecast.map(item => ({
    date: new Date(item.ds).toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    }),
    forecast: parseFloat(item.yhat),
    forecastUpper: parseFloat(item.yhat_upper),
    forecastLower: parseFloat(item.yhat_lower),
    type: 'forecast'
  }));

  // Find the last historical date
  // This will now match the new format (e.g., "Dec 10, 2023") automatically
  const lastHistoricalDate = historicalData[historicalData.length - 1]?.date;

  // Combine data
  const allData = [...historicalData, ...forecastData];

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="tooltip-label">{`Date: ${label}`}</p>
          {payload.map((entry, index) => {
            if (entry.dataKey === 'forecastLower' || entry.dataKey === 'forecastUpper') return null;
            const value = entry.value.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            let label = entry.name;
            let color = entry.color || '#667eea';
            
            if (entry.dataKey === 'actual') {
              label = 'Actual Cost';
              color = '#667eea';
            } else if (entry.dataKey === 'forecast') {
              label = 'Forecast';
              color = '#28a745';
            }
            
            return (
              <p key={index} className="tooltip-value" style={{ color }}>
                <span className="tooltip-dot" style={{ background: color }}></span>
                {label}: <strong>₹{value}</strong>
              </p>
            );
          })}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height={550}>
        <ComposedChart data={allData} margin={{ top: 10, right: 30, left: 0, bottom: 60 }}>
          <defs>
            <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#28a745" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#28a745" stopOpacity={0.05}/>
            </linearGradient>
            <linearGradient id="colorUncertainty" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#ffc107" stopOpacity={0.2}/>
              <stop offset="95%" stopColor="#ffc107" stopOpacity={0.05}/>
            </linearGradient>
            <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#667eea" stopOpacity={0.4}/>
              <stop offset="95%" stopColor="#667eea" stopOpacity={0.1}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" opacity={0.5} />
          <XAxis 
            dataKey="date" 
            angle={-45}
            textAnchor="end"
            height={80}
            stroke="#666"
            style={{ fontSize: '12px' }}
            tick={{ fill: '#666' }}
          />
          <YAxis 
            stroke="#666"
            style={{ fontSize: '12px' }}
            tick={{ fill: '#666' }}
            tickFormatter={(value) => `₹${(value / 1000).toFixed(0)}k`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="line"
          />
          
          {/* Shaded area for forecast uncertainty (between upper and lower) */}
          <Area
            type="monotone"
            dataKey="forecastUpper"
            stroke="none"
            fill="url(#colorUncertainty)"
            name="Confidence Interval"
            connectNulls
          />
          <Area
            type="monotone"
            dataKey="forecastLower"
            stroke="none"
            fill="#fff"
            fillOpacity={1}
            name=""
            connectNulls
          />
          
          {/* Historical actual cost area */}
          <Area
            type="monotone"
            dataKey="actual"
            stroke="none"
            fill="url(#colorActual)"
            name=""
            connectNulls
            hide
          />
          
          {/* Historical actual cost line */}
          <Line 
            type="monotone" 
            dataKey="actual" 
            stroke="#667eea" 
            strokeWidth={3}
            name="Actual Cost"
            dot={false}
            activeDot={{ r: 6, fill: '#667eea', stroke: '#fff', strokeWidth: 2 }}
          />
          
          {/* Forecast line */}
          <Line 
            type="monotone" 
            dataKey="forecast" 
            stroke="#28a745" 
            strokeWidth={3}
            strokeDasharray="8 4"
            name="Forecast"
            dot={false}
            activeDot={{ r: 6, fill: '#28a745', stroke: '#fff', strokeWidth: 2 }}
          />
          
          {/* Upper bound line */}
          <Line 
            type="monotone" 
            dataKey="forecastUpper" 
            stroke="#ffc107" 
            strokeWidth={2}
            strokeDasharray="4 4"
            name="Upper Bound"
            dot={false}
            connectNulls
          />
          
          {/* Lower bound line */}
          <Line 
            type="monotone" 
            dataKey="forecastLower" 
            stroke="#ffc107" 
            strokeWidth={2}
            strokeDasharray="4 4"
            name="Lower Bound"
            dot={false}
            connectNulls
          />
          
          {/* Reference line to separate historical and future */}
          {lastHistoricalDate && (
            <ReferenceLine 
              x={lastHistoricalDate} 
              stroke="#dc3545" 
              strokeWidth={2}
              strokeDasharray="4 4"
              label={{ value: "Today", position: "top", fill: "#dc3545", fontSize: 12, fontWeight: 'bold' }}
            />
          )}
        </ComposedChart>
      </ResponsiveContainer>
      
      {/* Future shaded region indicator */}
      <div className="forecast-info">
        <div className="legend-item">
          <span className="info-box actual"></span>
          <span>Historical Data</span>
        </div>
        <div className="legend-item">
          <span className="info-box forecast"></span>
          <span>Future Forecast</span>
        </div>
        <div className="legend-item">
          <span className="info-box uncertainty"></span>
          <span>Confidence Interval</span>
        </div>
      </div>
    </div>
  );
}

export default ForecastChart;