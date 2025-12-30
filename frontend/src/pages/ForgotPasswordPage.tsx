import React, { useState } from 'react';
import { AuthLayout } from '../components/auth/AuthLayout';
import { ForgotPasswordForm } from '../components/auth/ForgotPasswordForm';
import { ResetPasswordForm } from '../components/auth/ResetPasswordForm';

export const ForgotPasswordPage: React.FC = () => {
  const [userId, setUserId] = useState<string | null>(null);

  return (
    <AuthLayout title={userId ? 'Reset Password' : 'Forgot Password'}>
      {userId ? (
        <ResetPasswordForm userId={userId} />
      ) : (
        <ForgotPasswordForm onSuccess={setUserId} />
      )}
      <div style={styles.footer}>
        <a href="/login" style={styles.link}>
          Back to Login
        </a>
      </div>
    </AuthLayout>
  );
};

const styles = {
  footer: {
    textAlign: 'center' as const,
    marginTop: '24px',
    fontSize: '14px',
  },
  link: {
    color: '#1e40af',
    textDecoration: 'none',
    fontWeight: '600',
  },
};
