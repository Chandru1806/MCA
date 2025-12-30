import React, { useState, useRef } from 'react';
import { TermsModal } from './TermsModal';

interface PDFUploaderProps {
  onFileSelect: (file: File, bank: string) => void;
  disabled: boolean;
}

export const PDFUploader: React.FC<PDFUploaderProps> = ({ onFileSelect, disabled }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedBank, setSelectedBank] = useState<string>('AUTO');
  const [error, setError] = useState<string>('');
  const [isDragging, setIsDragging] = useState(false);
  const [showTermsModal, setShowTermsModal] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (!disabled) setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (disabled) return;

    const file = e.dataTransfer.files[0];
    validateAndSetFile(file);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) validateAndSetFile(file);
  };

  const validateAndSetFile = (file: File) => {
    if (file.type !== 'application/pdf') {
      setError('Only PDF files are allowed');
      setSelectedFile(null);
      return;
    }
    setError('');
    setSelectedFile(file);
  };

  const handleUpload = () => {
    if (!selectedFile) {
      setError('Please select a file');
      return;
    }
    if (selectedBank === 'AUTO') {
      setError('Please select a bank');
      return;
    }
    setError('');
    onFileSelect(selectedFile, selectedBank);
  };

  const formatFileSize = (bytes: number): string => {
    return (bytes / 1024 / 1024).toFixed(2) + ' MB';
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>PDF Upload</h3>
      
      <div
        style={{
          ...styles.dropzone,
          ...(isDragging ? styles.dropzoneActive : {}),
          ...(disabled ? styles.dropzoneDisabled : {}),
        }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !disabled && fileInputRef.current?.click()}
      >
        <p style={styles.dropzoneText}>Drag and drop your PDF here</p>
        <p style={styles.dropzoneSubtext}>or click to browse</p>
        <input
          ref={fileInputRef}
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          style={styles.fileInput}
          disabled={disabled}
        />
      </div>

      {selectedFile && (
        <div style={styles.fileInfo}>
          <p style={styles.fileName}>{selectedFile.name}</p>
          <p style={styles.fileSize}>{formatFileSize(selectedFile.size)}</p>
        </div>
      )}

      <div style={styles.bankSection}>
        <label style={styles.label}>Select Bank</label>
        <select
          value={selectedBank}
          onChange={(e) => {
            if (e.target.value !== 'AUTO') {
              setShowTermsModal(true);
            }
            setSelectedBank(e.target.value);
          }}
          style={styles.select}
          disabled={disabled}
        >
          {/* <option value="AUTO">Auto-detect or select manually</option> */}
          <option value="HDFC">HDFC</option>
          <option value="KOTAK">KOTAK</option>
          <option value="SBI">SBI</option>
          <option value="ICICI">ICICI</option>
          <option value="AXIS">AXIS</option>
          <option value="CUB">CUB</option>
          <option value="IDFC">IDFC</option>
        </select>
      </div>

      <TermsModal isOpen={showTermsModal} onClose={() => setShowTermsModal(false)} />

      {error && <p style={styles.error}>{error}</p>}

      <button
        onClick={handleUpload}
        disabled={disabled || !selectedFile || selectedBank === 'AUTO'}
        style={{
          ...styles.button,
          ...(disabled || !selectedFile || selectedBank === 'AUTO' ? styles.buttonDisabled : {}),
        }}
      >
        Upload
      </button>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    padding: '20px',
  },
  title: {
    fontSize: '16px',
    fontWeight: 'bold',
    marginBottom: '15px',
    color: '#1a1a1a',
  },
  dropzone: {
    border: '2px dashed #cbd5e0',
    borderRadius: '8px',
    padding: '40px 20px',
    textAlign: 'center',
    cursor: 'pointer',
    backgroundColor: '#f7fafc',
    transition: 'all 0.3s',
  },
  dropzoneActive: {
    borderColor: '#4299e1',
    backgroundColor: '#ebf8ff',
  },
  dropzoneDisabled: {
    cursor: 'not-allowed',
    opacity: 0.6,
  },
  dropzoneText: {
    fontSize: '14px',
    color: '#4a5568',
    margin: '0 0 5px 0',
  },
  dropzoneSubtext: {
    fontSize: '12px',
    color: '#718096',
    margin: 0,
  },
  fileInput: {
    display: 'none',
  },
  fileInfo: {
    marginTop: '15px',
    padding: '10px',
    backgroundColor: '#edf2f7',
    borderRadius: '6px',
  },
  fileName: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#2d3748',
    margin: '0 0 5px 0',
  },
  fileSize: {
    fontSize: '12px',
    color: '#718096',
    margin: 0,
  },
  bankSection: {
    marginTop: '20px',
  },
  label: {
    display: 'block',
    fontSize: '14px',
    fontWeight: '500',
    marginBottom: '8px',
    color: '#2d3748',
  },
  select: {
    width: '100%',
    padding: '10px',
    fontSize: '14px',
    border: '1px solid #cbd5e0',
    borderRadius: '6px',
    backgroundColor: '#fff',
    cursor: 'pointer',
  },
  error: {
    color: '#e53e3e',
    fontSize: '13px',
    marginTop: '10px',
  },
  button: {
    width: '100%',
    padding: '12px',
    marginTop: '20px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#fff',
    backgroundColor: '#4299e1',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  },
  buttonDisabled: {
    backgroundColor: '#a0aec0',
    cursor: 'not-allowed',
  },
};
