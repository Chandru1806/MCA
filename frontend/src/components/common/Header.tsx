import React from 'react';
import { LOGO_PATH } from '../../utils/constants';

export const Header: React.FC = () => {
  return (
    <header style={styles.header}>
      <div style={styles.container}>
        <div style={styles.logoSection}>
          <img src={LOGO_PATH} alt="ExpenseIQ" style={styles.logo} />
          <div>
            <h1 style={styles.title}>ExpenseIQ</h1>
            <p style={styles.tagline}>Smart personal expense and budget advisor</p>
          </div>
        </div>
      </div>
    </header>
  );
};

const styles = {
  header: {
    backgroundColor: '#ffffff',
    borderBottom: '1px solid #e5e7eb',
    padding: '16px 0',
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 20px',
  },
  logoSection: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  logo: {
    height: '40px',
    width: 'auto',
  },
  title: {
    fontSize: '24px',
    fontWeight: '700',
    color: '#1e40af',
    margin: '0',
    letterSpacing: '-0.5px',
  },
  tagline: {
    fontSize: '12px',
    color: '#6b7280',
    margin: '2px 0 0 0',
    fontWeight: '400',
  },
};