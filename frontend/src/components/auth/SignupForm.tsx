import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '../common/Input';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { authController } from '../../controllers/authController';

export const SignupForm: React.FC = () => {
  const navigate = useNavigate();
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<{ firstName?: string; lastName?: string; username?: string; email?: string; password?: string; confirmPassword?: string }>({});
  const [apiError, setApiError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setApiError('');

    const validationErrors = authController.validateSignup(firstName, lastName, username, email, password, confirmPassword);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setLoading(true);

    const result = await authController.handleSignup({ first_name: firstName, last_name: lastName, username, email, password, confirmPassword });

    setLoading(false);

    if (result.success) {
      navigate('/dashboard');
    } else {
      setApiError(result.error || 'Signup failed');
    }
  };

  if (loading) {
    return (
      <div style={styles.loadingContainer}>
        <LoadingSpinner size="medium" />
        <p style={styles.loadingText}>Creating account...</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      {apiError && (
        <div style={styles.errorBox}>{apiError}</div>
      )}

      <Input
        type="text"
        label="First Name"
        value={firstName}
        onChange={(e) => setFirstName(e.target.value)}
        placeholder="Enter your first name"
        error={errors.firstName}
        required
      />

      <Input
        type="text"
        label="Last Name"
        value={lastName}
        onChange={(e) => setLastName(e.target.value)}
        placeholder="Enter your last name"
        error={errors.lastName}
        required
      />

      <Input
        type="text"
        label="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Enter a username"
        error={errors.username}
        required
      />

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
        Create Account
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
