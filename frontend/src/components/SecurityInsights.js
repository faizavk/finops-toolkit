import React from 'react';
import './SecurityInsights.css';

function SecurityInsights({ insights }) {
  if (!insights) {
    return <div className="no-data">No security insights available</div>;
  }

  const { extreme_spikes, rare_tags, rare_tags_by_frequency, new_tags } = insights;

  return (
    <div className="security-insights">
      <div className="insight-section">
        <h3>🚨 Extreme Cost Spikes</h3>
        <p className="insight-description">
          Dates where actual cost exceeded 10x the predicted cost
        </p>
        {extreme_spikes && extreme_spikes.length > 0 ? (
          <div className="spikes-list">
            {extreme_spikes.map((spike, index) => (
              <div key={index} className="spike-item">
                <div className="spike-date">
                  {new Date(spike.ds).toLocaleDateString()}
                </div>
                <div className="spike-details">
                  <span>Actual: ₹{parseFloat(spike.y).toFixed(2)}</span>
                  <span>Predicted: ₹{parseFloat(spike.yhat).toFixed(2)}</span>
                  <span className="spike-ratio">
                    {parseFloat(spike.spike_ratio).toFixed(2)}x
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="no-issues">No extreme spikes detected ✓</p>
        )}
      </div>

      <div className="insight-section">
        <h3>🏷️ Rare Tags</h3>
        <p className="insight-description">
          Tags that appear infrequently or are new
        </p>
        {rare_tags && rare_tags.length > 0 ? (
          <div className="tags-list">
            {rare_tags.map((tag, index) => (
              <span key={index} className="tag-badge rare">{tag}</span>
            ))}
          </div>
        ) : (
          <p className="no-issues">No rare tags found ✓</p>
        )}
      </div>

      <div className="insight-section">
        <h3>📊 Rare Tags by Frequency</h3>
        <p className="insight-description">
          Tags that appear in bottom 10% of frequency distribution
        </p>
        {rare_tags_by_frequency && rare_tags_by_frequency.length > 0 ? (
          <div className="tags-list">
            {rare_tags_by_frequency.map((tag, index) => (
              <span key={index} className="tag-badge frequency">{tag}</span>
            ))}
          </div>
        ) : (
          <p className="no-issues">No rare tags by frequency ✓</p>
        )}
      </div>

      <div className="insight-section">
        <h3>🆕 New Tags</h3>
        <p className="insight-description">
          Tags that appeared recently (last 30 days) but not before
        </p>
        {new_tags && new_tags.length > 0 ? (
          <div className="tags-list">
            {new_tags.map((tag, index) => (
              <span key={index} className="tag-badge new">{tag}</span>
            ))}
          </div>
        ) : (
          <p className="no-issues">No new tags detected ✓</p>
        )}
      </div>
    </div>
  );
}

export default SecurityInsights;

