import React from 'react';

// Tüm asset görsellerini al
const images = require.context('../assets', false, /\.(png|jpe?g|svg)$/);

export default function Card({ product }) {
  let productImage;

  try {
    productImage = images(`./${product.image}`);
  } catch (error) {
    console.warn(`Görsel bulunamadı: ${product.image}`);
    productImage = null;
  }

  return (
    <div className="bg-white shadow-lg rounded-2xl overflow-hidden hover:shadow-2xl transition-shadow">
      <div className="w-full h-48 flex items-center justify-center bg-white p-2">
        {productImage ? (
          <img src={productImage} alt={product.name} className="max-h-full object-contain" />
        ) : (
          <div className="text-red-500">Görsel yok</div>
        )}
      </div>
      <div className="p-4">
        <h2 className="text-lg font-semibold mb-2">{product.name}</h2>
        <p className="text-gray-600 mb-4">{product.description}</p>
      </div>
    </div>
  );
}
