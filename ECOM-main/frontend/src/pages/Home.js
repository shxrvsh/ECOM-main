import React from 'react';

const Home = () => (
  <div className="products-container" style={{ textAlign: 'center' }}>
    <h2 className="products-title">Welcome to ECOM!</h2>
    <p style={{ fontSize: '1.2rem', color: '#555', margin: '24px 0' }}>
      Your one-stop shop for all your needs.<br />
      Browse products, manage your cart, and enjoy a seamless shopping experience.
    </p>
    <p style={{ color: '#2980b9', fontWeight: 'bold' }}>
      Please login or register to get started.
    </p>
  </div>
);

export default Home;