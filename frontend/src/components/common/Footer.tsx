import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer style={styles.footer}>
      <div style={styles.container}>
        <p style={styles.text}>
          © 2025 ExpenseIQ. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

const styles = {
  footer: {
    backgroundColor: '#f7f8fa',
    borderTop: '1px solid #e5e7eb',
    padding: '20px 0',
    marginTop: 'auto',
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 20px',
    textAlign: 'left' as const,
  },
  text: {
    fontSize: '14px',
    color: '#6b7280',
    margin: '0',
  },
};