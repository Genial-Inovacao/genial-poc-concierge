import React, { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../store/AuthContext';
import { 
  HomeIcon, 
  UserIcon, 
  ClockIcon,
  Bars3Icon,
  XMarkIcon,
  ArrowRightOnRectangleIcon 
} from '@heroicons/react/24/outline';

const Layout = () => {
  const location = useLocation();
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'Perfil', href: '/profile', icon: UserIcon },
    { name: 'Histórico', href: '/history', icon: ClockIcon },
  ];

  const isActive = (path) => location.pathname === path;

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-xl font-bold text-primary-600">
                  {import.meta.env.VITE_APP_NAME}
                </h1>
              </div>
              
              {/* Desktop Navigation */}
              <div className="hidden sm:ml-8 sm:flex sm:space-x-8">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                      isActive(item.href)
                        ? 'border-primary-500 text-gray-900'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <item.icon className="w-5 h-5 mr-2" />
                    {item.name}
                  </Link>
                ))}
              </div>
            </div>

            {/* Desktop User Menu */}
            <div className="hidden sm:ml-6 sm:flex sm:items-center">
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700">
                  Olá, {user?.name?.split(' ')[0]}
                </span>
                <button
                  onClick={handleLogout}
                  className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-gray-500 bg-white hover:text-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  <ArrowRightOnRectangleIcon className="w-5 h-5 mr-2" />
                  Sair
                </button>
              </div>
            </div>

            {/* Mobile menu button */}
            <div className="flex items-center sm:hidden">
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
              >
                {mobileMenuOpen ? (
                  <XMarkIcon className="block h-6 w-6" />
                ) : (
                  <Bars3Icon className="block h-6 w-6" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="sm:hidden">
            <div className="pt-2 pb-3 space-y-1">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`block pl-3 pr-4 py-2 border-l-4 text-base font-medium ${
                    isActive(item.href)
                      ? 'bg-primary-50 border-primary-500 text-primary-700'
                      : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700'
                  }`}
                >
                  <div className="flex items-center">
                    <item.icon className="w-5 h-5 mr-3" />
                    {item.name}
                  </div>
                </Link>
              ))}
            </div>
            <div className="pt-4 pb-3 border-t border-gray-200">
              <div className="flex items-center px-4">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-primary-500 flex items-center justify-center">
                    <span className="text-white font-medium">
                      {user?.name?.charAt(0).toUpperCase()}
                    </span>
                  </div>
                </div>
                <div className="ml-3">
                  <div className="text-base font-medium text-gray-800">
                    {user?.name}
                  </div>
                  <div className="text-sm font-medium text-gray-500">
                    {user?.email}
                  </div>
                </div>
              </div>
              <div className="mt-3 space-y-1">
                <button
                  onClick={handleLogout}
                  className="block w-full text-left px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
                >
                  Sair
                </button>
              </div>
            </div>
          </div>
        )}
      </nav>

      {/* Page Content */}
      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;