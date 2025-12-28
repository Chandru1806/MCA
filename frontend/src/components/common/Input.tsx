import React from 'react';

interface InputProps {
  type?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  label?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
}

export const Input: React.FC<InputProps> = ({
  type = 'text',
  value,
  onChange,
  placeholder,
  label,
  error,
  required = false,
  disabled = false,
}) => {
  return (
    <div style={styles.container}>
      {label && (
        <label style={styles.label}>
          {label} {required && <span style={styles.required}>*</span>}
        </label>
      )}
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        disabled={disabled}
        style={{
          ...styles.input,
          ...(error ? styles.inputError : {}),
          ...(disabled ? styles.inputDisabled : {}),
        }}
      />
      {error && <span style={styles.error}>{error}</span>}
    </div>
  );
};

const styles = {
  container: {
    marginBottom: '24px',
  },
  label: {
    display: 'block',
    fontSize: '14px',
    fontWeight: '500',
    color: '#374151',
    marginBottom: '8px',
  },
  required: {
    color: '#dc2626',
  },
  input: {
    width: '100%',
    padding: '12px 16px',
    fontSize: '15px',
    color: '#111827',
    backgroundColor: '#ffffff',
    border: '1px solid #d1d5db',
    borderRadius: '8px',
    outline: 'none',
    transition: 'border-color 0.2s, box-shadow 0.2s',
    boxSizing: 'border-box' as const,
  },
  inputError: {
    borderColor: '#dc2626',
  },
  inputDisabled: {
    backgroundColor: '#f3f4f6',
    cursor: 'not-allowed',
  },
  error: {
    display: 'block',
    fontSize: '13px',
    color: '#dc2626',
    marginTop: '6px',
  },
};
