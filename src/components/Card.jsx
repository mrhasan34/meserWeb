import React from 'react';

export default function Card({ product }) {
  return (
    <div className="bg-white shadow-lg rounded-2xl overflow-hidden hover:shadow-2xl transition-shadow">
      <div className="w-full h-48 flex items-center justify-center bg-white p-2">
        <img src={product.imageUrl} alt={product.name} className="max-h-full object-contain" />
      </div>
      <div className="p-4">
        <h2 className="text-lg font-semibold mb-2">{product.name}</h2>
        <p className="text-gray-600 mb-4">{product.description}</p>
        <span className="text-purple-600 font-bold">{product.price} ₺</span>
      </div>
    </div>
  );
}