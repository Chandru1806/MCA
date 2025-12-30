import React, { useRef } from 'react';

interface CSVUploaderProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
}

export const CSVUploader: React.FC<CSVUploaderProps> = ({ onFileSelect, selectedFile }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onFileSelect(file);
  };

  return (
    <div style={styles.container}>
      <div style={styles.uploadBox} onClick={() => fileInputRef.current?.click()}>
        <p style={styles.uploadText}>Click to select CSV file</p>
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          style={styles.fileInput}
        />
      </div>
      {selectedFile && (
        <div style={styles.fileInfo}>
          <p style={styles.fileName}>{selectedFile.name}</p>
          <p style={styles.fileSize}>{(selectedFile.size / 1024).toFixed(2)} KB</p>
        </div>
      )}
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    width: '100%',
  },
  uploadBox: {
    border: '2px dashed #cbd5e0',
    borderRadius: '8px',
    padding: '40px 20px',
    textAlign: 'center',
    cursor: 'pointer',
    backgroundColor: '#f7fafc',
  },
  uploadText: {
    fontSize: '14px',
    color: '#4a5568',
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
};
