import React from 'react';

interface PreprocessResultProps {
  fileName: string;
  onDownload: () => void;
  onReset: () => void;
}

export const PreprocessResult: React.FC<PreprocessResultProps> = ({ fileName, onDownload, onReset }) => {
  return (
    <div style={styles.container}>
      <div style={styles.successIcon}>✓</div>
      <h3 style={styles.title}>Preprocessing Complete</h3>
      <p style={styles.message}>Your CSV has been normalized and repaired</p>
      <p style={styles.fileName}>{fileName}</p>
      <button onClick={onDownload} style={styles.downloadButton}>
        Download Normalized CSV
      </button>
      <button onClick={onReset} style={styles.resetButton}>
        Process Another File
      </button>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    textAlign: 'center',
    padding: '40px 20px',
  },
  successIcon: {
    width: '60px',
    height: '60px',
    margin: '0 auto 20px',
    backgroundColor: '#48bb78',
    color: '#fff',
    fontSize: '32px',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#2d3748',
    margin: '0 0 10px 0',
  },
  message: {
    fontSize: '14px',
    color: '#718096',
    margin: '0 0 20px 0',
  },
  fileName: {
    fontSize: '13px',
    color: '#4a5568',
    backgroundColor: '#edf2f7',
    padding: '8px 12px',
    borderRadius: '6px',
    margin: '0 0 20px 0',
    display: 'inline-block',
  },
  downloadButton: {
    width: '100%',
    padding: '12px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#fff',
    backgroundColor: '#4299e1',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    marginBottom: '10px',
  },
  resetButton: {
    width: '100%',
    padding: '12px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#4a5568',
    backgroundColor: '#edf2f7',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
  },
};
