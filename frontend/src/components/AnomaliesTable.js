import React from 'react';
import './AnomaliesTable.css';

function AnomaliesTable({ anomalies, onAnomalyClick }) {
  if (!anomalies || anomalies.length === 0) {
    return <div className="no-data">No anomalies detected</div>;
  }

  return (
    <div className="anomalies-table-container">
      <table className="anomalies-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Actual Cost</th>
            <th>Predicted Cost</th>
            <th>Deviation</th>
            <th>Deviation %</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {anomalies.map((anomaly, index) => (
            <tr key={index} className="anomaly-row">
              <td>{anomaly.date}</td>
              <td className="cost-cell">₹{anomaly.actual_cost.toFixed(2)}</td>
              <td className="cost-cell">₹{anomaly.predicted_cost.toFixed(2)}</td>
              <td className={`deviation-cell ${anomaly.deviation > 0 ? 'positive' : 'negative'}`}>
                ₹{anomaly.deviation.toFixed(2)}
              </td>
              <td className={`deviation-cell ${anomaly.deviation > 0 ? 'positive' : 'negative'}`}>
                {anomaly.deviation_percent.toFixed(2)}%
              </td>
              <td>
                <button 
                  className="btn-rca"
                  onClick={() => onAnomalyClick(anomaly)}
                >
                  View RCA
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AnomaliesTable;

