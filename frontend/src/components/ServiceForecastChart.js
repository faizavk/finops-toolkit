import React from 'react';
import {
  ComposedChart,
  Area,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  defs,
  linearGradient,
  stop
} from 'recharts';
import './ServiceForecastChart.css';

function ServiceForecastChart({ data }) {
  if (!data || !data.long || data.long.length === 0) {
    return <div className="no-data">No service forecast data available. Click "Service Forecast" to generate.</div>;
  }

  // Group by date and prepare data for chart
  const dateMap = {};
  
  data.long.forEach(item => {
    const date = item.date;
    if (!dateMap[date]) {
      // UPDATED: Added year: 'numeric' to the formatting options
      dateMap[date] = { 
        date: new Date(date).toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'short', 
          day: 'numeric' 
        }) 
      };
    }
    dateMap[date][item.service] = item.forecast;
  });

  // Ensure chronological ordering: Object.values preserves insertion order which
  // can be non-chronological when `data.long` is grouped by service. Sort the
  // ISO date keys so the chart x-axis is time-ordered.
  const chartData = Object.keys(dateMap).sort().map(k => dateMap[k]);
  
  // Get all unique services for colors
  const services = [...new Set(data.long.map(item => item.service))];
  
  // Color palette
  const colors = [
    '#667eea', '#764ba2', '#28a745', '#ffc107', '#dc3545',
    '#17a2b8', '#6f42c1', '#e83e8c', '#fd7e14', '#20c997'
  ];

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="tooltip-label">{`Date: ${label}`}</p>
          {payload.map((entry, index) => (
            <p key={index} className="tooltip-value" style={{ color: entry.color }}>
              <span className="tooltip-dot" style={{ background: entry.color }}></span>
              {entry.name}: <strong>₹{entry.value.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong>
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="service-chart-container">
      <ResponsiveContainer width="100%" height={500}>
        <ComposedChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 60 }}>
          <defs>
            {services.map((service, index) => (
              <linearGradient key={service} id={`color${index}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={colors[index % colors.length]} stopOpacity={0.6}/>
                <stop offset="95%" stopColor={colors[index % colors.length]} stopOpacity={0.1}/>
              </linearGradient>
            ))}
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
          
          {/* Stacked areas for each service */}
          {services.map((service, index) => (
            <Area
              key={service}
              type="monotone"
              dataKey={service}
              stackId="1"
              stroke={colors[index % colors.length]}
              fill={`url(#color${index})`}
              name={service}
            />
          ))}
        </ComposedChart>
      </ResponsiveContainer>
      
      <div className="service-legend">
        <p className="legend-title">Service Forecast Breakdown</p>
        <div className="service-list">
          {services.map((service, index) => (
            <div key={service} className="service-item">
              <span className="service-color" style={{ background: colors[index % colors.length] }}></span>
              <span>{service}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ServiceForecastChart;