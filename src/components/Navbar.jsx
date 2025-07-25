import React from 'react';
import { NavLink, useLocation, Link } from 'react-router-dom';
import logo from '../assets/logo.png';

const Navbar = ({ onSearchChange, searchTerm }) => {
  const location = useLocation();
  const showSearch = location.pathname === '/products';

  return (
    <nav className="bg-purple-800 text-white p-4 flex justify-between items-center sticky top-0 z-50 shadow-lg">
      <div className="flex items-center">
        <img src={logo} alt="Logo" className="h-10 w-10 mr-3" />
        <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-fuchsia-500 to-yellow-400 text-2xl font-extrabold tracking-wide drop-shadow-lg select-none">MESER</span>
      </div>

      {showSearch && (
        <div className="flex-grow max-w-xl mx-4">
          <input
            type="text"
            value={searchTerm}
            onChange={e => onSearchChange(e.target.value)}
            placeholder="Ürün ara..."
            className="w-full px-4 py-2 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-purple-300 shadow-sm"
          />
        </div>
      )}

      <div className="flex space-x-4 mt-2 sm:mt-0">
        <NavLink
          to="/products"
          className={({ isActive }) =>
            `px-3 py-2 rounded-md text-white hover:bg-purple-700 transition-colors whitespace-nowrap ${isActive ? 'bg-purple-800' : ''}`
          }
        >
          TELEFON
        </NavLink>
        <NavLink
          to="/contact"
          className={({ isActive }) =>
            `px-3 py-2 rounded-md text-white hover:bg-purple-700 transition-colors whitespace-nowrap ${isActive ? 'bg-purple-800' : ''}`
          }
        >
          İLETİŞİM
        </NavLink>
      </div>
    </nav>
  );
};

export default Navbar;