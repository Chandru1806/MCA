import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '../common/Input';
import { authController } from '../../controllers/authController';

export const SignupForm: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; password?: string; confirmPassword?: string }>({});
  const [apiError, setApiError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setApiError('');

    const validationErrors = authController.validateSignup(email, password, confirmPassword);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setLoading(true);

    const result = await authController.handleSignup({ email, password, confirmPassword });

    setLoading(false);

    if (result.success) {
      navigate('/dashboard');
    } else {
      setApiError(result.error || 'Signup failed');
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
        placeholder="Create a strong password"
        error={errors.password}
        required
      />

      <Input
        type="password"
        label="Confirm Password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        placeholder="Re-enter your password"
        error={errors.confirmPassword}
        required
      />

      <button type="submit" disabled={loading} style={{
        ...styles.button,
        ...(loading ? styles.buttonDisabled : {}),
      }}>
        {loading ? 'Creating account...' : 'Create Account'}
      </button>

      <div style={styles.footer}>
        Already have an account?{' '}
        <a href="/login" style={styles.link}>
          Login
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
