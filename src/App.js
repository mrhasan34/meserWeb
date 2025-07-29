import React, { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Products from './pages/Products';
import ContactPage from './pages/ContactPage.jsx';

export default function App() {
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar searchTerm={searchTerm} onSearchChange={setSearchTerm} />
      <div className="p-6">
        <Routes>
          <Route path="/" element={<Navigate to="/products" />} />
          <Route path="/products" element={<Products searchTerm={searchTerm} />} />
          <Route path="/contact" element={<ContactPage />} />
        </Routes>
      </div>
    </div>
  );
}
