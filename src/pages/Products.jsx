import React, { useEffect, useState } from 'react';
import Card from '../components/Card';
import productsData from '../data/products.json';

export default function Products({ searchTerm }) {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    setProducts(productsData);
  }, []);

  const filtered = products.filter(p =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map(p => (
          <Card key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
}
