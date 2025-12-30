import React, { useEffect } from 'react';
import PreferenceForm from './PreferenceForm';
import { PreferenceFormData } from '../../models/Preference';

interface PreferenceModalProps {
  isOpen: boolean;
  initialData: PreferenceFormData;
  onClose: () => void;
  onSubmit: (data: PreferenceFormData) => void;
  isLoading: boolean;
}

const PreferenceModal: React.FC<PreferenceModalProps> = ({
  isOpen,
  initialData,
  onClose,
  onSubmit,
  isLoading,
}) => {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div style={styles.overlay} onClick={handleOverlayClick}>
      <div style={styles.modal}>
        <div style={styles.header}>
          <h2 style={styles.title}>Edit Preferences</h2>
          <button style={styles.closeButton} onClick={onClose} disabled={isLoading}>
            &times;
          </button>
        </div>
        <div style={styles.content}>
          <PreferenceForm
            initialData={initialData}
            onSubmit={onSubmit}
            onCancel={onClose}
            isLoading={isLoading}
          />
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
    borderRadius: '8px',
    width: '90%',
    maxWidth: '500px',
    maxHeight: '90vh',
    overflow: 'auto',
    boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '20px 24px',
    borderBottom: '1px solid #e5e7eb',
  },
  title: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#111827',
  },
  closeButton: {
    fontSize: '28px',
    fontWeight: '300',
    color: '#6b7280',
    backgroundColor: 'transparent',
    border: 'none',
    cursor: 'pointer',
    padding: '0',
    width: '32px',
    height: '32px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: '4px',
    transition: 'background-color 0.2s',
  },
  content: {
    padding: '24px',
  },
};

export default PreferenceModal;
