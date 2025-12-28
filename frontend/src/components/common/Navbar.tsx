import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { LOGO_PATH } from '../../utils/constants';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-md px-6 py-4">
      <div className="flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center">
          <img src={LOGO_PATH} alt="ExpenseIQ" className="h-10" />
        </Link>
        
        <div className="flex items-center gap-6">
          <Link to="/dashboard" className="text-gray-700 hover:text-blue-600">Dashboard</Link>
          <Link to="/upload" className="text-gray-700 hover:text-blue-600">Upload</Link>
          <Link to="/analytics" className="text-gray-700 hover:text-blue-600">Analytics</Link>
          
          <div className="flex items-center gap-3 border-l pl-6">
            <span className="text-sm text-gray-600">{user?.email}</span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};
