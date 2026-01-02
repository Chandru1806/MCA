import React, { useState } from 'react';
import { CSVUploader } from '../components/common/CSVUploader';
import { PreprocessProgress } from '../components/common/PreprocessProgress';
import { PreprocessResult } from '../components/common/PreprocessResult';
import { preprocessController } from '../controllers/preprocessController';

type Step = 'select' | 'confirm' | 'processing' | 'complete';

export const PreprocessPage: React.FC = () => {
  const [step, setStep] = useState<Step>('select');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [processedBlob, setProcessedBlob] = useState<Blob | null>(null);
  const [error, setError] = useState<string>('');
  const [successMessage, setSuccessMessage] = useState<string>('');

  const handleFileSelect = (file: File) => {
    const validation = preprocessController.validateFile(file);
    if (!validation.valid) {
      setError(validation.error || 'Invalid file');
      return;
    }
    setError('');
    setSelectedFile(file);
    setStep('confirm');
  };

  const handleConfirm = async () => {
    if (!selectedFile) return;
    
    setStep('processing');
    setError('');

    try {
      const blob = await preprocessController.processCSV(selectedFile);
      setProcessedBlob(blob);
      setSuccessMessage('File processed successfully! You can now download it.');
      setStep('complete');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Processing failed');
      setStep('confirm');
    }
  };

  const handleDownload = () => {
    if (processedBlob && selectedFile) {
      preprocessController.downloadFile(processedBlob, selectedFile.name);
    }
  };

  const handleReset = () => {
    setStep('select');
    setSelectedFile(null);
    setProcessedBlob(null);
    setError('');
    setSuccessMessage('');
  };

  const handleBack = () => {
    setStep('select');
    setSelectedFile(null);
    setError('');
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.heading}>Data Preprocessing</h2>
        
        <div style={styles.stepIndicator}>
          <div style={step === 'select' ? styles.stepActive : styles.stepComplete}>
            {step === 'select' ? '1' : '✓'}
          </div>
          <div style={styles.stepLine}></div>
          <div style={['confirm', 'processing', 'complete'].includes(step) ? styles.stepActive : styles.stepInactive}>
            {['processing', 'complete'].includes(step) ? '✓' : '2'}
          </div>
          <div style={styles.stepLine}></div>
          <div style={step === 'processing' ? styles.stepActive : step === 'complete' ? styles.stepComplete : styles.stepInactive}>
            {step === 'complete' ? '✓' : '3'}
          </div>
          <div style={styles.stepLine}></div>
          <div style={step === 'complete' ? styles.stepActive : styles.stepInactive}>4</div>
        </div>

        <div style={styles.stepLabels}>
          <span style={styles.stepLabel}>Select</span>
          <span style={styles.stepLabel}>Confirm</span>
          <span style={styles.stepLabel}>Process</span>
          <span style={styles.stepLabel}>Download</span>
        </div>

        {error && (
          <div style={styles.error}>{error}</div>
        )}

        {successMessage && (
          <div style={styles.success}>{successMessage}</div>
        )}

        {step === 'select' && (
          <CSVUploader onFileSelect={handleFileSelect} selectedFile={selectedFile} />
        )}

        {step === 'confirm' && selectedFile && (
          <div style={styles.confirmSection}>
            <h3 style={styles.confirmTitle}>Confirm File</h3>
            <div style={styles.fileDetails}>
              <p style={styles.fileDetailLabel}>File Name:</p>
              <p style={styles.fileDetailValue}>{selectedFile.name}</p>
              <p style={styles.fileDetailLabel}>File Size:</p>
              <p style={styles.fileDetailValue}>{(selectedFile.size / 1024).toFixed(2)} KB</p>
            </div>
            <div style={styles.buttonGroup}>
              <button onClick={handleBack} style={styles.backButton}>Back</button>
              <button onClick={handleConfirm} style={styles.confirmButton}>Upload & Process</button>
            </div>
          </div>
        )}

        {step === 'processing' && <PreprocessProgress />}

        {step === 'complete' && selectedFile && (
          <PreprocessResult
            fileName={selectedFile.name.replace('.csv', '_NORMALIZED.csv')}
            onDownload={handleDownload}
            onReset={handleReset}
          />
        )}
      </div>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f7fafc',
    padding: '40px 20px',
  },
  card: {
    maxWidth: '600px',
    margin: '0 auto',
    backgroundColor: '#fff',
    borderRadius: '12px',
    padding: '30px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  heading: {
    fontSize: '24px',
    fontWeight: '700',
    color: '#1a1a1a',
    margin: '0 0 30px 0',
    textAlign: 'center',
  },
  stepIndicator: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: '10px',
  },
  stepActive: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    backgroundColor: '#4299e1',
    color: '#fff',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '16px',
    fontWeight: '600',
  },
  stepComplete: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    backgroundColor: '#48bb78',
    color: '#fff',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '16px',
    fontWeight: '600',
  },
  stepInactive: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    backgroundColor: '#e2e8f0',
    color: '#a0aec0',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '16px',
    fontWeight: '600',
  },
  stepLine: {
    flex: 1,
    height: '2px',
    backgroundColor: '#e2e8f0',
    margin: '0 10px',
  },
  stepLabels: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '30px',
  },
  stepLabel: {
    fontSize: '12px',
    color: '#718096',
    width: '40px',
    textAlign: 'center',
  },
  error: {
    padding: '12px',
    backgroundColor: '#fff5f5',
    border: '1px solid #fc8181',
    borderRadius: '6px',
    color: '#c53030',
    fontSize: '14px',
    marginBottom: '20px',
  },
  success: {
    padding: '12px',
    backgroundColor: '#f0fdf4',
    border: '1px solid #86efac',
    borderRadius: '6px',
    color: '#16a34a',
    fontSize: '14px',
    marginBottom: '20px',
  },
  confirmSection: {
    padding: '20px 0',
  },
  confirmTitle: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#2d3748',
    marginBottom: '20px',
  },
  fileDetails: {
    backgroundColor: '#f7fafc',
    padding: '15px',
    borderRadius: '8px',
    marginBottom: '20px',
  },
  fileDetailLabel: {
    fontSize: '13px',
    color: '#718096',
    margin: '0 0 5px 0',
  },
  fileDetailValue: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#2d3748',
    margin: '0 0 15px 0',
  },
  buttonGroup: {
    display: 'flex',
    gap: '10px',
  },
  backButton: {
    flex: 1,
    padding: '12px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#4a5568',
    backgroundColor: '#edf2f7',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
  },
  confirmButton: {
    flex: 2,
    padding: '12px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#fff',
    backgroundColor: '#4299e1',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
  },
};
