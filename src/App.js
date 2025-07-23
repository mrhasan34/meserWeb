import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Products from './pages/Products';

export default function App() {
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar searchTerm={searchTerm} onSearchChange={setSearchTerm} />
      <div className="p-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<Products searchTerm={searchTerm} />} />
        </Routes>
      </div>
    </div>
  );
}
