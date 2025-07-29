import React, { useState } from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Products from './pages/Products';

export default function App() {
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <HashRouter>
      <div className="min-h-screen bg-gray-100">
        <Navbar searchTerm={searchTerm} onSearchChange={setSearchTerm} />
        <div className="p-6">
          <Routes>
            <Route path="/" element={<Navigate to="/products" replace />} />
            <Route path="/products" element={<Products searchTerm={searchTerm} />} />
            <Route path="/contact" element={<Home />} />
          </Routes>
        </div>
      </div>
    </HashRouter>
  );
}
