import React, { useState } from 'react';

interface TermsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const TermsModal: React.FC<TermsModalProps> = ({ isOpen, onClose }) => {
  const [isChecked, setIsChecked] = useState(false);

  if (!isOpen) return null;

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setIsChecked(e.target.checked);
    if (e.target.checked) {
      setTimeout(() => onClose(), 300);
    }
  };

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <h2 style={styles.header}>Terms & Conditions</h2>
        
        <div style={styles.content}>
          <h3 style={styles.subHeader}>Account Statement Upload Guidelines</h3>
          <ul style={styles.list}>
            <li style={styles.listItem}>Only PDF format is supported</li>
            <li style={styles.listItem}>Supported banks: SBI, HDFC, ICICI, KOTAK, AXIS, CUB, IDFC</li>
            <li style={styles.listItem}>Your data is encrypted and secure</li>
            <li style={styles.listItem}>Maximum file size: 10 MB</li>
          </ul>
        </div>

        <div style={styles.checkboxContainer}>
          <input
            type="checkbox"
            id="terms-checkbox"
            checked={isChecked}
            onChange={handleCheckboxChange}
            style={styles.checkbox}
          />
          <label htmlFor="terms-checkbox" style={styles.checkboxLabel}>
            I agree to the terms and conditions
          </label>
        </div>
      </div>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
  },
  modal: {
    backgroundColor: '#fff',
    width: '500px',
    padding: '30px',
    borderRadius: '8px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
  },
  header: {
    fontSize: '16pt',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '20px',
    marginTop: 0,
  },
  content: {
    marginBottom: '25px',
  },
  subHeader: {
    fontSize: '14pt',
    fontWeight: '600',
    color: '#555',
    marginBottom: '15px',
    marginTop: 0,
  },
  list: {
    paddingLeft: '20px',
    margin: 0,
  },
  listItem: {
    color: '#666',
    fontSize: '12pt',
    lineHeight: '1.6',
    marginBottom: '8px',
  },
  checkboxContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  checkbox: {
    width: '18px',
    height: '18px',
    cursor: 'pointer',
    accentColor: '#007bff',
  },
  checkboxLabel: {
    fontSize: '12pt',
    color: '#333',
    cursor: 'pointer',
    userSelect: 'none',
  },
};
