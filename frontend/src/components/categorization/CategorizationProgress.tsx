import React from 'react';

interface Props {
  current: number;
  total: number;
  status: string;
}

export const CategorizationProgress: React.FC<Props> = ({ current, total, status }) => {
  const percentage = total > 0 ? Math.round((current / total) * 100) : 0;

  return (
    <div style={{ textAlign: 'center', padding: '40px 20px' }}>
      <div style={{
        width: '60px',
        height: '60px',
        border: '4px solid #f3f3f3',
        borderTop: '4px solid #50C878',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite',
        margin: '0 auto 20px'
      }} />
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
      <h3 style={{ margin: '0 0 16px', fontSize: '18px', color: '#333' }}>{status}</h3>
      <div style={{
        width: '100%',
        maxWidth: '400px',
        height: '8px',
        backgroundColor: '#e0e0e0',
        borderRadius: '4px',
        margin: '0 auto 12px',
        overflow: 'hidden'
      }}>
        <div style={{
          width: `${percentage}%`,
          height: '100%',
          backgroundColor: '#50C878',
          transition: 'width 0.3s ease'
        }} />
      </div>
      <p style={{ margin: 0, fontSize: '14px', color: '#666' }}>
        {current} / {total} ({percentage}%)
      </p>
    </div>
  );
};
