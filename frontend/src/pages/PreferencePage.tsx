import React, { useEffect, useState } from 'react';
import PreferenceModal from '../components/preference/PreferenceModal';
import { preferenceService } from '../services/preferenceService';
import { Preference, PreferenceFormData } from '../models/Preference';
import { useToast } from '../hooks/useToast';

const PreferencePage: React.FC = () => {
  const [preference, setPreference] = useState<Preference | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);
  const { showToast } = useToast();

  const fetchPreferences = async () => {
    try {
      setIsFetching(true);
      const data = await preferenceService.getPreferences();
      setPreference(data);
    } catch (error: any) {
      showToast(error.response?.data?.message || 'Failed to load preferences', 'error');
    } finally {
      setIsFetching(false);
    }
  };

  useEffect(() => {
    fetchPreferences();
  }, []);

  const handleSubmit = async (formData: PreferenceFormData) => {
    try {
      setIsLoading(true);
      const updated = await preferenceService.updatePreferences(formData);
      setPreference(updated);
      setIsModalOpen(false);
      showToast('Preferences updated successfully', 'success');
    } catch (error: any) {
      showToast(error.response?.data?.message || 'Failed to update preferences', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  if (isFetching) {
    return (
      <div style={styles.container}>
        <div style={styles.loading}>Loading preferences...</div>
      </div>
    );
  }

  if (!preference) {
    return (
      <div style={styles.container}>
        <div style={styles.error}>Failed to load preferences</div>
      </div>
    );
  }

  const formData: PreferenceFormData = {
    phone: preference.phone || '',
    address_line_1: preference.address_line_1 || '',
    address_line_2: preference.address_line_2 || '',
    city: preference.city || '',
    state: preference.state || '',
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <h1 style={styles.title}>User Preferences</h1>
          <button style={styles.editButton} onClick={() => setIsModalOpen(true)}>
            Edit
          </button>
        </div>

        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Personal Information</h2>
          <div style={styles.grid}>
            <div style={styles.field}>
              <span style={styles.label}>First Name</span>
              <span style={styles.value}>{preference.first_name}</span>
            </div>
            <div style={styles.field}>
              <span style={styles.label}>Last Name</span>
              <span style={styles.value}>{preference.last_name}</span>
            </div>
            <div style={styles.field}>
              <span style={styles.label}>Username</span>
              <span style={styles.value}>{preference.username}</span>
            </div>
            <div style={styles.field}>
              <span style={styles.label}>Email</span>
              <span style={styles.value}>{preference.email}</span>
            </div>
          </div>
        </div>

        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Contact Information</h2>
          <div style={styles.grid}>
            <div style={styles.field}>
              <span style={styles.label}>Phone</span>
              <span style={styles.value}>{preference.phone || 'Not provided'}</span>
            </div>
            <div style={styles.field}>
              <span style={styles.label}>Address Line 1</span>
              <span style={styles.value}>{preference.address_line_1 || 'Not provided'}</span>
            </div>
            <div style={styles.field}>
              <span style={styles.label}>Address Line 2</span>
              <span style={styles.value}>{preference.address_line_2 || 'Not provided'}</span>
            </div>
            <div style={styles.field}>
              <span style={styles.label}>City</span>
              <span style={styles.value}>{preference.city || 'Not provided'}</span>
            </div>
            <div style={styles.field}>
              <span style={styles.label}>State</span>
              <span style={styles.value}>{preference.state || 'Not provided'}</span>
            </div>
          </div>
        </div>
      </div>

      <PreferenceModal
        isOpen={isModalOpen}
        initialData={formData}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleSubmit}
        isLoading={isLoading}
      />
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    padding: '24px',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  loading: {
    textAlign: 'center',
    padding: '48px',
    fontSize: '16px',
    color: '#6b7280',
  },
  error: {
    textAlign: 'center',
    padding: '48px',
    fontSize: '16px',
    color: '#ef4444',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    overflow: 'hidden',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '24px',
    borderBottom: '1px solid #e5e7eb',
  },
  title: {
    fontSize: '24px',
    fontWeight: '600',
    color: '#111827',
  },
  editButton: {
    padding: '8px 16px',
    fontSize: '14px',
    fontWeight: '500',
    color: '#fff',
    backgroundColor: '#2563eb',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  section: {
    padding: '24px',
    borderBottom: '1px solid #e5e7eb',
  },
  sectionTitle: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#111827',
    marginBottom: '16px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '16px',
  },
  field: {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
  },
  label: {
    fontSize: '13px',
    fontWeight: '500',
    color: '#6b7280',
  },
  value: {
    fontSize: '14px',
    color: '#111827',
  },
};

export default PreferencePage;
