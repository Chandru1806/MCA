import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '../common/Input';
import { authController } from '../../controllers/authController';

export const LoginForm: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  const [apiError, setApiError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setApiError('');

    const validationErrors = authController.validateLogin(email, password);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setLoading(true);

    const result = await authController.handleLogin({ email, password });

    setLoading(false);

    if (result.success) {
      navigate('/dashboard');
    } else {
      setApiError(result.error || 'Login failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {apiError && (
        <div style={styles.errorBox}>{apiError}</div>
      )}

      <Input
        type="email"
        label="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email address"
        error={errors.email}
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
        {loading ? 'Logging in...' : 'Login'}
      </button>

      <div style={styles.footer}>
        Don't have an account?{' '}
        <a href="/signup" style={styles.link}>
          Sign up
        </a>
      </div>
    </form>
  );
};

const styles = {
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
