import React from 'react';
import '../styles/spinner.css';

export const PreprocessProgress: React.FC = () => {
  return (
    <div style={styles.container}>
      <div style={styles.spinner}></div>
      <p style={styles.text}>Processing CSV...</p>
      <p style={styles.subtext}>Repairing missing transaction data</p>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    textAlign: 'center',
    padding: '40px 20px',
  },
  spinner: {
    width: '40px',
    height: '40px',
    margin: '0 auto 20px',
    border: '4px solid #e2e8f0',
    borderTop: '4px solid #4299e1',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  text: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#2d3748',
    margin: '0 0 8px 0',
  },
  subtext: {
    fontSize: '14px',
    color: '#718096',
    margin: 0,
  },
};
