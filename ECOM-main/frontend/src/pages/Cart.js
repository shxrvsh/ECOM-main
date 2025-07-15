import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { getUserId } from '../utils/auth';

const Cart = () => {
  const [cart, setCart] = useState([]);

  useEffect(() => {
    const userId = getUserId();
    if (!userId) return;
    axios.get(`http://localhost:5050/api/cart/${userId}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }).then(res => {
      setCart(res.data);
    });
  }, []);

  const handleRemove = (id) => {
    axios.delete(`http://localhost:5050/api/cart/${id}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }).then(() => {
      setCart(cart.filter(item => item.id !== id));
    });
  };

  const handleClear = () => {
    const userId = getUserId();
    axios.delete(`http://localhost:5050/api/cart/user/${userId}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }).then(() => {
      setCart([]);
    });
  };

  return (
    <div className="cart-container">
      <h2 className="cart-title">Your Cart</h2>
      <button className="cart-clear-btn" onClick={handleClear}>Clear Cart</button>
      <ul className="cart-list">
        {cart.length === 0 ? (
          <li style={{ textAlign: 'center', color: '#888' }}>Your cart is empty.</li>
        ) : (
          cart.map(item => (
            <li className="cart-item" key={item.id}>
              <div className="cart-details">
                <strong>{item.name}</strong>
                <div>₹{item.price} x {item.quantity}</div>
              </div>
              <button className="cart-remove-btn" onClick={() => handleRemove(item.id)}>Remove</button>
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default Cart;