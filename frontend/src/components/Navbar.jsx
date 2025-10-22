import React from 'react';
import { Menu, Bell, User, LogOut } from 'lucide-react';

export default function Navbar({ onMenuClick }) {
  return (
    <nav className="bg-white border-b border-gray-200 shadow-sm">
      <div className="px-4 md:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          {/* Left side - Menu and Logo */}
          <div className="flex items-center gap-4">
            <button
              onClick={onMenuClick}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors md:hidden"
              aria-label="Toggle menu"
            >
              <Menu size={24} className="text-gray-600" />
            </button>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">MV</span>
              </div>
              <h1 className="text-xl font-bold text-gray-900 hidden sm:block">
                Genomics Variants
              </h1>
            </div>
          </div>

          {/* Right side - Actions */}
          <div className="flex items-center gap-4">
            <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors relative">
              <Bell size={20} className="text-gray-600" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            
          
          </div>
        </div>
      </div>
    </nav>
  );
}
