// src/components/Sidebar.tsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export const Sidebar = () => {
  const location = useLocation();

  const links = [
    { path: '/', label: 'Dashboard' },
    { path: '/analysis', label: 'Analysis' },
    { path: '/reports', label: 'Reports' }
  ];

  return (
    <div className="w-64 bg-gray-800 text-white p-6 h-screen">
      <div className="mb-8">
        <h1 className="text-xl font-bold">MSE Analysis</h1>
      </div>
      <nav className="space-y-4">
        {links.map(link => (
          <Link
            key={link.path}
            to={link.path}
            className={`block py-2 px-4 rounded ${
              location.pathname === link.path 
                ? 'bg-blue-600' 
                : 'hover:bg-gray-700'
            }`}
          >
            {link.label}
          </Link>
        ))}
      </nav>
    </div>
  );
};