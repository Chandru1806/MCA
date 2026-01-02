import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export const Sidebar: React.FC = () => {
  const location = useLocation();

  const links = [
    { path: '/dashboard', label: 'Dashboard' },
  ];

  return (
    <aside style={styles.sidebar}>
      <nav style={styles.nav}>
        {links.map((link) => (
          <Link
            key={link.path}
            to={link.path}
            style={{
              ...styles.link,
              ...(location.pathname === link.path ? styles.activeLink : styles.inactiveLink),
            }}
          >
            {link.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
};

const styles = {
  sidebar: {
    width: '110px',
    backgroundColor: '#ffffff',
    borderRight: '1px solid #e5e7eb',
    minHeight: '0vh',
    // padding: '20px 16px',
  },
  nav: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '8px',
  },
  link: {
    display: 'block',
    padding: '12px 16px',
    borderRadius: '8px',
    textDecoration: 'none',
    fontSize: '15px',
    fontWeight: '500',
    transition: 'all 0.2s ease',
  },
  activeLink: {
    backgroundColor: '#2563eb',
    color: '#ffffff',
  },
  inactiveLink: {
    backgroundColor: 'transparent',
    color: '#374151',
  },
};
