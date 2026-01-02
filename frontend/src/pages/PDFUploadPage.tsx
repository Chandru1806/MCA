import React, { useState } from 'react';
import { PDFUploader } from '../components/common/PDFUploader';
import { UploadProgress } from '../components/common/UploadProgress';
import { UploadResult } from '../components/common/UploadResult';
import { pdfController } from '../controllers/pdfController';
import { PDFUploadResponse } from '../models/PDFUploadResponse';

export const PDFUploadPage: React.FC = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('');
  const [result, setResult] = useState<PDFUploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleFileSelect = async (file: File, bank: string) => {
    const fileError = pdfController.validateFile(file);
    const bankError = pdfController.validateBank(bank);

    if (fileError || bankError) {
      setError(fileError || bankError);
      return;
    }

    setIsUploading(true);
    setProgress(0);
    setStatus('Uploading PDF...');
    setError(null);
    setResult(null);

    try {
      setProgress(10);
      setStatus('Extracting transactions...');

      const uploadResult = await pdfController.handleUpload(file, bank, (prog) => {
        setProgress(prog);
        if (prog === 100) setStatus('Processing data...');
      });

      setResult(uploadResult);
      setStatus('Upload completed successfully');
      setSuccessMessage('PDF uploaded and processed successfully!');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
      setStatus('Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  const handleRetry = () => {
    setResult(null);
    setError(null);
    setSuccessMessage(null);
    setProgress(0);
    setStatus('');
  };

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <h1 style={styles.title}>Upload Bank Statement</h1>
        <p style={styles.description}>
          Upload your bank statement PDF to extract and analyze transactions
        </p>
      </div>

      <div style={styles.card}>
        {successMessage && (
          <div style={styles.successBox}>{successMessage}</div>
        )}
        <PDFUploader onFileSelect={handleFileSelect} disabled={isUploading} />

        {isUploading && <UploadProgress progress={progress} status={status} />}

        <UploadResult result={result} error={error} onRetry={handleRetry} />
      </div>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: '100vh',
    backgroundColor: '#f7fafc',
    padding: '40px 20px',
  },
  header: {
    textAlign: 'center',
    marginBottom: '30px',
  },
  title: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#1a202c',
    marginBottom: '10px',
  },
  description: {
    fontSize: '14px',
    color: '#718096',
    maxWidth: '600px',
    margin: '0 auto',
  },
  card: {
    maxWidth: '700px',
    margin: '0 auto',
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    overflow: 'hidden',
  },
  successBox: {
    backgroundColor: '#f0fdf4',
    color: '#16a34a',
    padding: '12px 16px',
    margin: '20px',
    borderRadius: '8px',
    fontSize: '14px',
    border: '1px solid #86efac',
  },
};
