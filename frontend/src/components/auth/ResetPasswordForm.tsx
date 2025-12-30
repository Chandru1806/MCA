import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '../common/Input';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { forgotPasswordController } from '../../controllers/forgotPasswordController';

interface ResetPasswordFormProps {
  userId: string;
}

export const ResetPasswordForm: React.FC<ResetPasswordFormProps> = ({ userId }) => {
  const navigate = useNavigate();
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<{ password?: string; confirmPassword?: string }>({});
  const [apiError, setApiError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setApiError('');

    const validationErrors = forgotPasswordController.validatePassword(password, confirmPassword);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setLoading(true);

    const result = await forgotPasswordController.handleResetPassword(userId, { password });

    setLoading(false);

    if (result.success) {
      navigate('/login');
    } else {
      setApiError(result.error || 'Password reset failed');
    }
  };

  if (loading) {
    return (
      <div style={styles.loadingContainer}>
        <LoadingSpinner size="medium" />
        <p style={styles.loadingText}>Resetting password...</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      {apiError && <div style={styles.errorBox}>{apiError}</div>}

      <Input
        type="password"
        label="New Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter new password"
        error={errors.password}
        required
      />

      <Input
        type="password"
        label="Confirm Password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        placeholder="Confirm new password"
        error={errors.confirmPassword}
        required
      />

      <div style={styles.passwordRules}>
        <p style={styles.rulesTitle}>Password must contain:</p>
        <ul style={styles.rulesList}>
          <li>At least 8 characters</li>
          <li>One uppercase letter</li>
          <li>One lowercase letter</li>
          <li>One number</li>
        </ul>
      </div>

      <button type="submit" disabled={loading} style={styles.button}>
        Reset Password
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
  errorBox: {
    backgroundColor: '#fef2f2',
    color: '#dc2626',
    padding: '12px 16px',
    borderRadius: '8px',
    marginBottom: '24px',
    fontSize: '14px',
    border: '1px solid #fecaca',
  },
  passwordRules: {
    backgroundColor: '#f9fafb',
    padding: '16px',
    borderRadius: '8px',
    marginTop: '16px',
    marginBottom: '24px',
  },
  rulesTitle: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#374151',
    marginBottom: '8px',
  },
  rulesList: {
    margin: 0,
    paddingLeft: '20px',
    fontSize: '13px',
    color: '#6b7280',
    lineHeight: '1.8',
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
  },
};
