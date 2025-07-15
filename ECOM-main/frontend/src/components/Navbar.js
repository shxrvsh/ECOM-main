import React from 'react';
import { Link } from 'react-router-dom';

function getRole() {
  const token = localStorage.getItem('token');
  if (!token) return null;
  try {
    return JSON.parse(atob(token.split('.')[1])).role;
  } catch {
    return null;
  }
}

export default function Navbar() {
  const role = getRole();

  return (
    <nav>
      <Link to="/">Home</Link>
      {(!role || role !== 'admin') && (
        <>
          <Link to="/products">Products</Link>
          <Link to="/cart">Cart</Link>
        </>
      )}
      {role === 'admin' && <Link to="/admin">Admin</Link>}
      <Link to="/login">Login</Link>
      <Link to="/register">Register</Link>
    </nav>
  );
}