import React from 'react';
import {
  AreaChart,
  Area,
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
import './CostChart.css';

function CostChart({ data }) {
  if (!data || data.length === 0) {
    return <div className="no-data">No historical data available</div>;
  }

  const chartData = data.map(item => ({
    date: new Date(item.ds).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    cost: parseFloat(item.y)
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="tooltip-label">{`Date: ${label}`}</p>
          <p className="tooltip-value">
            <span className="tooltip-dot"></span>
            Cost: <strong>₹{payload[0].value.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height={450}>
        <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 60 }}>
          <defs>
            <linearGradient id="colorCost" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#667eea" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#764ba2" stopOpacity={0.1}/>
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
          <Area 
            type="monotone" 
            dataKey="cost" 
            stroke="#667eea" 
            strokeWidth={3}
            fill="url(#colorCost)"
            name="Daily Cost (INR)"
            dot={false}
            activeDot={{ r: 6, fill: '#667eea', stroke: '#fff', strokeWidth: 2 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export default CostChart;

