import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Products from './pages/Products';
import Cart from './pages/Cart';
import Admin from './pages/Admin';
import Navbar from './components/Navbar';
import Home from './pages/Home'; // Create a simple Home.js page
import Register from './pages/Register'; // Import the Register page
import './App.css'; // Assuming you have some styles in App.css

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/register" element={<Register />} /> {/* Add the Register route */}
      </Routes>
    </Router>
  );
}

export default App;