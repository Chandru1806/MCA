import React from 'react';
import { AuthLayout } from '../components/auth/AuthLayout';
import { SignupForm } from '../components/auth/SignupForm';

export const SignupPage: React.FC = () => {
  return (
    <AuthLayout 
      title="Create your account" 
      subtitle="Start managing your expenses smartly and take control of your budget."
    >
      <SignupForm />
    </AuthLayout>
  );
};
