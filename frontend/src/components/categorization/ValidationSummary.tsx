import React from 'react';

interface Props {
  total: number;
  valid: number;
  rejected: number;
  onViewRejected?: () => void;
}

export const ValidationSummary: React.FC<Props> = ({ total, valid, rejected, onViewRejected }) => {
  return (
    <div style={{
      display: 'flex',
      gap: '20px',
      padding: '12px 16px',
      backgroundColor: '#f5f5f5',
      borderRadius: '4px',
      marginBottom: '16px',
      alignItems: 'center'
    }}>
      <div style={{ flex: 1 }}>
        <span style={{ fontSize: '14px', color: '#666' }}>Total Rows: </span>
        <span style={{ fontSize: '16px', fontWeight: 'bold' }}>{total}</span>
      </div>
      <div style={{ flex: 1 }}>
        <span style={{ fontSize: '14px', color: '#388e3c' }}>Valid: </span>
        <span style={{ fontSize: '16px', fontWeight: 'bold', color: '#388e3c' }}>{valid}</span>
      </div>
      <div style={{ flex: 1 }}>
        <span style={{ fontSize: '14px', color: '#d32f2f' }}>Rejected: </span>
        <span style={{ fontSize: '16px', fontWeight: 'bold', color: '#d32f2f' }}>{rejected}</span>
        {rejected > 0 && onViewRejected && (
          <button
            onClick={onViewRejected}
            style={{
              marginLeft: '8px',
              padding: '4px 8px',
              fontSize: '12px',
              backgroundColor: 'transparent',
              border: '1px solid #d32f2f',
              color: '#d32f2f',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            View
          </button>
        )}
      </div>
    </div>
  );
};
