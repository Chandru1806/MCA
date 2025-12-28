import React from 'react';

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({ children, title, subtitle }) => {
  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <h1 style={styles.logo}>ExpenseIQ</h1>
          <p style={styles.tagline}>Smart personal expense and budget advisor</p>
        </div>
        
        <div style={styles.content}>
          <h2 style={styles.title}>{title}</h2>
          {subtitle && <p style={styles.subtitle}>{subtitle}</p>}
          {children}
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f7f8fa',
    padding: '20px',
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
    width: '100%',
    maxWidth: '440px',
    overflow: 'hidden',
  },
  header: {
    backgroundColor: '#f7f8fa',
    padding: '32px 40px 24px',
    textAlign: 'center' as const,
    borderBottom: '1px solid #e5e7eb',
  },
  logo: {
    fontSize: '32px',
    fontWeight: '700',
    color: '#1e40af',
    margin: '0 0 8px 0',
    letterSpacing: '-0.5px',
  },
  tagline: {
    fontSize: '13px',
    color: '#6b7280',
    margin: 0,
    fontWeight: '400',
  },
  content: {
    padding: '40px',
  },
  title: {
    fontSize: '24px',
    fontWeight: '600',
    color: '#111827',
    margin: '0 0 8px 0',
  },
  subtitle: {
    fontSize: '14px',
    color: '#6b7280',
    margin: '0 0 32px 0',
    lineHeight: '1.5',
  },
};
