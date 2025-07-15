import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { getUserId } from '../utils/auth';

const Products = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5050/api/products').then(res => {
      setProducts(res.data);
    });
  }, []);

  const handleAddToCart = (productId) => {
    const userId = getUserId();
    if (!userId) {
      alert('Please login first!');
      return;
    }
    axios.post(`http://localhost:5050/api/cart`, { user_id: userId, product_id: productId, quantity: 1 }, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(res => {
        alert('Added to cart!');
      });
  };

  return (
    <div className="products-container">
      <h2 className="products-title">Products</h2>
      <ul className="products-list">
        {products.map(product => (
          <li className="product-card" key={product.id}>
            {/* <img src={product.image} alt={product.name} /> */}
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <p>₹{product.price}</p>
            <button className="product-add-btn" onClick={() => handleAddToCart(product.id)}>
              Add to Cart
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Products;