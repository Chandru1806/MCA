import React, { useState } from 'react';
import { PreferenceFormData } from '../../models/Preference';

interface PreferenceFormProps {
  initialData: PreferenceFormData;
  onSubmit: (data: PreferenceFormData) => void;
  onCancel: () => void;
  isLoading: boolean;
}

const PreferenceForm: React.FC<PreferenceFormProps> = ({
  initialData,
  onSubmit,
  onCancel,
  isLoading,
}) => {
  const [formData, setFormData] = useState<PreferenceFormData>(initialData);
  const [errors, setErrors] = useState<Partial<Record<keyof PreferenceFormData, string>>>({});

  const validateForm = (): boolean => {
    const newErrors: Partial<Record<keyof PreferenceFormData, string>> = {};

    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone is required';
    } else if (!/^\d{10,15}$/.test(formData.phone.replace(/\s/g, ''))) {
      newErrors.phone = 'Phone must be 10-15 digits';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name as keyof PreferenceFormData]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <div style={styles.field}>
        <label style={styles.label}>Phone *</label>
        <input
          type="text"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          style={{ ...styles.input, ...(errors.phone ? styles.inputError : {}) }}
          disabled={isLoading}
        />
        {errors.phone && <span style={styles.error}>{errors.phone}</span>}
      </div>

      <div style={styles.field}>
        <label style={styles.label}>Address Line 1</label>
        <input
          type="text"
          name="address_line_1"
          value={formData.address_line_1}
          onChange={handleChange}
          style={styles.input}
          disabled={isLoading}
        />
      </div>

      <div style={styles.field}>
        <label style={styles.label}>Address Line 2</label>
        <input
          type="text"
          name="address_line_2"
          value={formData.address_line_2}
          onChange={handleChange}
          style={styles.input}
          disabled={isLoading}
        />
      </div>

      <div style={styles.field}>
        <label style={styles.label}>City</label>
        <input
          type="text"
          name="city"
          value={formData.city}
          onChange={handleChange}
          style={styles.input}
          disabled={isLoading}
        />
      </div>

      <div style={styles.field}>
        <label style={styles.label}>State</label>
        <input
          type="text"
          name="state"
          value={formData.state}
          onChange={handleChange}
          style={styles.input}
          disabled={isLoading}
        />
      </div>

      <div style={styles.buttonGroup}>
        <button type="submit" style={styles.saveButton} disabled={isLoading}>
          {isLoading ? 'Saving...' : 'Save'}
        </button>
        <button type="button" onClick={onCancel} style={styles.cancelButton} disabled={isLoading}>
          Cancel
        </button>
      </div>
    </form>
  );
};

const styles: Record<string, React.CSSProperties> = {
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  field: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
  },
  label: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#374151',
  },
  input: {
    padding: '10px 12px',
    fontSize: '14px',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    outline: 'none',
    transition: 'border-color 0.2s',
  },
  inputError: {
    borderColor: '#ef4444',
  },
  error: {
    fontSize: '12px',
    color: '#ef4444',
  },
  buttonGroup: {
    display: 'flex',
    gap: '12px',
    marginTop: '8px',
  },
  saveButton: {
    flex: 1,
    padding: '10px 16px',
    fontSize: '14px',
    fontWeight: '500',
    color: '#fff',
    backgroundColor: '#2563eb',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  cancelButton: {
    flex: 1,
    padding: '10px 16px',
    fontSize: '14px',
    fontWeight: '500',
    color: '#374151',
    backgroundColor: '#f3f4f6',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
};

export default PreferenceForm;
