import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '../common/Input';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { authController } from '../../controllers/authController';

export const LoginForm: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ username?: string; password?: string }>({});
  const [apiError, setApiError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setApiError('');

    const validationErrors = authController.validateLogin(username, password);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setLoading(true);

    const result = await authController.handleLogin({ username, password });

    setLoading(false);

    if (result.success) {
      setSuccessMessage('Login successful! Redirecting to dashboard...');
      setTimeout(() => navigate('/dashboard'), 1500);
    } else {
      setApiError(result.error || 'Login failed');
    }
  };

  if (loading) {
    return (
      <div style={styles.loadingContainer}>
        <LoadingSpinner size="medium" />
        <p style={styles.loadingText}>Logging in...</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      {successMessage && (
        <div style={styles.successBox}>{successMessage}</div>
      )}
      {apiError && (
        <div style={styles.errorBox}>{apiError}</div>
      )}

      <Input
        type="text"
        label="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Enter your username"
        error={errors.username}
        required
      />

      <Input
        type="password"
        label="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter your password"
        error={errors.password}
        required
      />

      <button type="submit" disabled={loading} style={{
        ...styles.button,
        ...(loading ? styles.buttonDisabled : {}),
      }}>
        Login
      </button>

      <div style={styles.footer}>
        <a href="/forgot-password" style={styles.link}>
          Forgot password?
        </a>
        <span style={{ margin: '0 8px', color: '#d1d5db' }}>|</span>
        Don't have an account?{' '}
        <a href="/signup" style={styles.link}>
          Sign up
        </a>
      </div>
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
  successBox: {
    backgroundColor: '#f0fdf4',
    color: '#16a34a',
    padding: '12px 16px',
    borderRadius: '8px',
    marginBottom: '24px',
    fontSize: '14px',
    border: '1px solid #86efac',
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
    transition: 'background-color 0.2s',
    marginTop: '8px',
  },
  buttonDisabled: {
    backgroundColor: '#93c5fd',
    cursor: 'not-allowed',
  },
  footer: {
    textAlign: 'center' as const,
    marginTop: '24px',
    fontSize: '14px',
    color: '#6b7280',
  },
  link: {
    color: '#1e40af',
    textDecoration: 'none',
    fontWeight: '600',
  },
};
