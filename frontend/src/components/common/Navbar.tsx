import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { LOGO_PATH } from '../../utils/constants';
import './Navbar.css';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };

    if (dropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [dropdownOpen]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const fullName = user ? `${user.first_name} ${user.last_name}` : '';

  return (
    <nav style={styles.nav}>
      <div style={styles.container}>
        <Link to="/dashboard" style={styles.logoLink}>
          <img src={LOGO_PATH} alt="ExpenseIQ" style={styles.logo} />
          <span style={styles.logoText}>ExpenseIQ</span>
        </Link>
        
        <div style={styles.userSection} ref={dropdownRef}>
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            style={styles.userButton}
            className="user-button"
          >
            {fullName}
            <span style={styles.arrow}>{dropdownOpen ? '▲' : '▼'}</span>
          </button>
          
          {dropdownOpen && (
            <div style={styles.dropdown}>
              <button
                onClick={() => {
                  setDropdownOpen(false);
                  navigate('/preferences');
                }}
                style={styles.dropdownItem}
                className="dropdown-item"
              >
                Preferences
              </button>
              <button
                onClick={() => {
                  setDropdownOpen(false);
                  handleLogout();
                }}
                style={styles.dropdownItem}
                className="dropdown-item"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

const styles = {
  nav: {
    backgroundColor: '#ffffff',
    borderBottom: '1px solid #e5e7eb',
    padding: '16px 0',
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  logoLink: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    textDecoration: 'none',
  },
  logo: {
    height: '40px',
    width: 'auto',
  },
  logoText: {
    fontSize: '24px',
    fontWeight: '700',
    color: '#1e40af',
    letterSpacing: '-0.5px',
  },
  userSection: {
    position: 'relative' as const,
  },
  userButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '8px 16px',
    backgroundColor: '#f3f4f6',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    fontSize: '14px',
    fontWeight: '500',
    color: '#374151',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  arrow: {
    fontSize: '10px',
    color: '#6b7280',
  },
  dropdown: {
    position: 'absolute' as const,
    top: '100%',
    right: '0',
    marginTop: '8px',
    backgroundColor: '#ffffff',
    border: '1px solid #e5e7eb',
    borderRadius: '6px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    minWidth: '180px',
    zIndex: 1000,
  },
  dropdownItem: {
    display: 'block',
    width: '100%',
    padding: '12px 16px',
    textAlign: 'left' as const,
    fontSize: '14px',
    color: '#374151',
    backgroundColor: 'transparent',
    border: 'none',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
};
