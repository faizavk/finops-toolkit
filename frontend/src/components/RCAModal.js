import React from 'react';
import './RCAModal.css';

function RCAModal({ anomaly, onClose }) {
  if (!anomaly || !anomaly.rca) {
    return null;
  }

  const { top_services, top_regions, top_tags } = anomaly.rca;

  const formatData = (data) => {
    return Object.entries(data)
      .sort((a, b) => b[1] - a[1])
      .map(([key, value]) => ({ name: key, value: parseFloat(value) }));
  };

  const services = formatData(top_services);
  const regions = formatData(top_regions);
  const tags = formatData(top_tags);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Root Cause Analysis</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        
        <div className="modal-body">
          <div className="anomaly-summary">
            <h3>Anomaly Details</h3>
            <p><strong>Date:</strong> {anomaly.date}</p>
            <p><strong>Actual Cost:</strong> ₹{anomaly.actual_cost.toFixed(2)}</p>
            <p><strong>Predicted Cost:</strong> ₹{anomaly.predicted_cost.toFixed(2)}</p>
            <p><strong>Deviation:</strong> ₹{anomaly.deviation.toFixed(2)} ({anomaly.deviation_percent.toFixed(2)}%)</p>
          </div>

          <div className="rca-section">
            <div className="rca-item">
              <h4>Top Services</h4>
              <ul>
                {services.map((item, index) => (
                  <li key={index}>
                    <span className="rca-name">{item.name}</span>
                    <span className="rca-value">₹{item.value.toFixed(2)}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="rca-item">
              <h4>Top Regions</h4>
              <ul>
                {regions.map((item, index) => (
                  <li key={index}>
                    <span className="rca-name">{item.name}</span>
                    <span className="rca-value">₹{item.value.toFixed(2)}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="rca-item">
              <h4>Top Tags</h4>
              <ul>
                {tags.map((item, index) => (
                  <li key={index}>
                    <span className="rca-name">{item.name}</span>
                    <span className="rca-value">₹{item.value.toFixed(2)}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RCAModal;

