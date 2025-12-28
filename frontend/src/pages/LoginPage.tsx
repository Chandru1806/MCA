import React from 'react';
import { AuthLayout } from '../components/auth/AuthLayout';
import { LoginForm } from '../components/auth/LoginForm';

export const LoginPage: React.FC = () => {
  return (
    <AuthLayout 
      title="Welcome back" 
      subtitle="Login to access your expense dashboard and budget insights."
    >
      <LoginForm />
    </AuthLayout>
  );
};
