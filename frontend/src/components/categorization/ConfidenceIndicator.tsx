import React from 'react';

interface Props {
  confidence: number;
}

export const ConfidenceIndicator: React.FC<Props> = ({ confidence }) => {
  const percentage = Math.round(confidence * 100);
  const color = percentage >= 90 ? '#27AE60' : percentage >= 70 ? '#F39C12' : '#E74C3C';

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
      <div style={{
        width: '60px',
        height: '6px',
        backgroundColor: '#e0e0e0',
        borderRadius: '3px',
        overflow: 'hidden'
      }}>
        <div style={{
          width: `${percentage}%`,
          height: '100%',
          backgroundColor: color,
          transition: 'width 0.3s ease'
        }} />
      </div>
      <span style={{ fontSize: '12px', color: '#666', minWidth: '35px' }}>{percentage}%</span>
    </div>
  );
};
