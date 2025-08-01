import React, { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';
import logo from '../assets/logo.png';

const Navbar = ({ onSearchChange, searchTerm }) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();

  // Sadece pathname’e bak, HashRouter olursa hash’ten, BrowserRouter olursa doğrudan history’den alır
  const showSearch = location.pathname === '/products';

  // Menü açıkken sayfa scroll’unu kapat
  useEffect(() => {
    document.body.style.overflow = menuOpen ? 'hidden' : 'auto';
  }, [menuOpen]);

  return (
    <nav className="bg-purple-800 text-white p-4 flex justify-between items-center sticky top-0 z-50 shadow-lg">
      {/* Logo */}
      <div className="flex items-center absolute left-4">
        <img src={logo} alt="Logo" className="h-10 w-10 mr-3" />
        <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-fuchsia-500 to-yellow-400 text-2xl font-extrabold tracking-wide drop-shadow-lg select-none">
          MESER
        </span>
      </div>

      {/* Search bar */}
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

      {/* Desktop Menü */}
      <div className="hidden md:flex space-x-4 mt-2 sm:mt-0">
        <NavLink
          to="/products"
          className={({ isActive }) =>
            `px-3 py-2 rounded-md text-white hover:bg-purple-700 transition-colors whitespace-nowrap ${isActive ? 'bg-purple-900' : ''
            }`
          }
        >
          TELEFON
        </NavLink>
        <NavLink
          to="/contact"
          className={({ isActive }) =>
            `px-3 py-2 rounded-md text-white hover:bg-purple-700 transition-colors whitespace-nowrap ${isActive ? 'bg-purple-900' : ''
            }`
          }
        >
          İLETİŞİM
        </NavLink>
      </div>

      {/* Mobile Menü butonu */}
      <div
        className="md:hidden cursor-pointer ml-2 z-50"
        onClick={() => setMenuOpen(o => !o)}
      >
        {menuOpen ? <AiOutlineClose size={26} /> : <AiOutlineMenu size={26} />}
      </div>

      {/* Mobile Menü */}
      {menuOpen && (
        <div className="absolute top-16 right-4 bg-purple-800 shadow-lg rounded-md flex flex-col w-40 md:hidden animate-slide-down">
          <NavLink
            to="/products"
            className="px-4 py-2 hover:bg-purple-700 rounded-t-md"
            onClick={() => setMenuOpen(false)}
          >
            TELEFON
          </NavLink>
          <NavLink
            to="/contact"
            className="px-4 py-2 hover:bg-purple-700 rounded-b-md"
            onClick={() => setMenuOpen(false)}
          >
            İLETİŞİM
          </NavLink>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
