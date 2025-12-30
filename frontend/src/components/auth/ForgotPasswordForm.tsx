import React, { useState } from 'react';
import { Input } from '../common/Input';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { forgotPasswordController } from '../../controllers/forgotPasswordController';

interface ForgotPasswordFormProps {
  onSuccess: (userId: string) => void;
}

export const ForgotPasswordForm: React.FC<ForgotPasswordFormProps> = ({ onSuccess }) => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [apiError, setApiError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setApiError('');

    const validationError = forgotPasswordController.validateEmail(email);
    if (validationError) {
      setError(validationError);
      return;
    }

    setError('');
    setLoading(true);

    const result = await forgotPasswordController.handleForgotPassword({ email });

    setLoading(false);

    if (result.success && result.userId) {
      onSuccess(result.userId);
    } else {
      setApiError(result.error || 'Failed to verify email');
    }
  };

  if (loading) {
    return (
      <div style={styles.loadingContainer}>
        <LoadingSpinner size="medium" />
        <p style={styles.loadingText}>Verifying email...</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      <p style={styles.helperText}>Enter your registered email to reset your password.</p>

      {apiError && <div style={styles.errorBox}>{apiError}</div>}

      <Input
        type="email"
        label="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
        error={error}
        required
      />

      <button type="submit" disabled={loading} style={styles.button}>
        Continue
      </button>
    </form>
  );
};

const styles = {
  loadingContainer: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    padding: '40px 0',
  },
  loadingText: {
    marginTop: '16px',
    fontSize: '14px',
    color: '#6b7280',
  },
  helperText: {
    fontSize: '14px',
    color: '#6b7280',
    marginBottom: '24px',
    lineHeight: '1.5',
  },
  errorBox: {
    backgroundColor: '#fef2f2',
    color: '#dc2626',
    padding: '12px 16px',
    borderRadius: '8px',
    marginBottom: '24px',
    fontSize: '14px',
    border: '1px solid #fecaca',
  },
  button: {
    width: '100%',
    padding: '14px',
    backgroundColor: '#1e40af',
    color: '#ffffff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
    marginTop: '8px',
  },
};
