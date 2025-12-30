import React from 'react';

interface UploadProgressProps {
  progress: number;
  status: string;
}

export const UploadProgress: React.FC<UploadProgressProps> = ({ progress, status }) => {
  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Upload Progress</h3>
      
      <div style={styles.progressContainer}>
        <div style={styles.progressBar}>
          <div style={{ ...styles.progressFill, width: `${progress}%` }} />
        </div>
        <span style={styles.progressText}>{progress}%</span>
      </div>

      <p style={styles.status}>{status}</p>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    padding: '20px',
    borderTop: '1px solid #e2e8f0',
  },
  title: {
    fontSize: '16px',
    fontWeight: 'bold',
    marginBottom: '15px',
    color: '#1a1a1a',
  },
  progressContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
  },
  progressBar: {
    flex: 1,
    height: '10px',
    backgroundColor: '#e2e8f0',
    borderRadius: '5px',
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#4299e1',
    transition: 'width 0.3s ease',
  },
  progressText: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#2d3748',
    minWidth: '45px',
  },
  status: {
    marginTop: '10px',
    fontSize: '13px',
    color: '#718096',
  },
};
