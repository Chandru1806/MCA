import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export const Sidebar: React.FC = () => {
  const location = useLocation();

  const links = [
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/upload', label: 'Upload Statement' },
    { path: '/transactions', label: 'Transactions' },
    { path: '/categorize', label: 'Categorize' },
    { path: '/analytics', label: 'Analytics' },
  ];

  return (
    <aside className="w-64 bg-gray-50 border-r min-h-screen p-4">
      <nav className="flex flex-col gap-2">
        {links.map((link) => (
          <Link
            key={link.path}
            to={link.path}
            className={`px-4 py-3 rounded transition-colors ${
              location.pathname === link.path
                ? 'bg-blue-600 text-white'
                : 'text-gray-700 hover:bg-gray-200'
            }`}
          >
            {link.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
};
