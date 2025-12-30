import React from 'react';
import { PDFUploadResponse } from '../../models/PDFUploadResponse';
import apiClient from '../../utils/apiClient';

interface UploadResultProps {
  result: PDFUploadResponse | null;
  error: string | null;
  onRetry: () => void;
}

export const UploadResult: React.FC<UploadResultProps> = ({ result, error, onRetry }) => {
  // Save statement_id to localStorage when result is available
  React.useEffect(() => {
    if (result?.statement_id) {
      localStorage.setItem('current_statement_id', result.statement_id.toString());
    }
  }, [result]);

  const handleDownload = async () => {
    if (!result?.csv_filename) return;
    
    try {
      const response = await apiClient.get(`/api/pdf/download/${result.csv_filename}`, {
        responseType: 'blob',
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.download = result.csv_filename;
      document.body.appendChild(link);
      link.click();
      link.parentChild?.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download failed:', error);
      alert('Failed to download CSV file');
    }
  };

  if (!result && !error) return null;

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Upload Result</h3>

      {error && (
        <div style={{ ...styles.card, ...styles.errorCard }}>
          <p style={styles.errorText}>{error}</p>
          <button onClick={onRetry} style={styles.retryButton}>
            Retry Upload
          </button>
        </div>
      )}

      {result && (
        <div style={{ ...styles.card, ...styles.successCard }}>
          <div style={styles.resultRow}>
            <span style={styles.label}>Detected Bank:</span>
            <span style={styles.value}>{result.bank_name}</span>
          </div>
          <div style={styles.resultRow}>
            <span style={styles.label}>Transaction Count:</span>
            <span style={styles.value}>{result.transaction_count}</span>
          </div>
          <div style={styles.resultRow}>
            <span style={styles.label}>Statement ID:</span>
            <span style={styles.value}>{result.statement_id}</span>
          </div>

          {result.csv_filename && (
            <button onClick={handleDownload} style={styles.downloadButton}>
              Download CSV
            </button>
          )}
        </div>
      )}
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
  card: {
    padding: '15px',
    borderRadius: '8px',
    border: '2px solid',
  },
  successCard: {
    borderColor: '#48bb78',
    backgroundColor: '#f0fff4',
  },
  errorCard: {
    borderColor: '#e53e3e',
    backgroundColor: '#fff5f5',
  },
  resultRow: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '10px',
  },
  label: {
    fontSize: '14px',
    color: '#4a5568',
    fontWeight: '500',
  },
  value: {
    fontSize: '14px',
    color: '#2d3748',
    fontWeight: '600',
  },
  errorText: {
    color: '#e53e3e',
    fontSize: '14px',
    marginBottom: '15px',
  },
  downloadButton: {
    width: '100%',
    padding: '10px',
    marginTop: '15px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#fff',
    backgroundColor: '#48bb78',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
  },
  retryButton: {
    width: '100%',
    padding: '10px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#fff',
    backgroundColor: '#e53e3e',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
  },
};
