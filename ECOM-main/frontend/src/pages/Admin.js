import React, { useState, useEffect } from 'react';
import axios from 'axios';

function getRole() {
  const token = localStorage.getItem('token');
  if (!token) return null;
  try {
    return JSON.parse(atob(token.split('.')[1])).role;
  } catch {
    return null;
  }
}

const Admin = () => {
  // Hooks must be called unconditionally
  const [products, setProducts] = useState([]);
  const [editing, setEditing] = useState(null);
  const [editData, setEditData] = useState({ name: '', description: '', price: '' });
  const [name, setName] = useState('');
  const [desc, setDesc] = useState('');
  const [price, setPrice] = useState('');

  useEffect(() => {
    axios.get('http://localhost:5050/api/products').then(res => setProducts(res.data));
  }, []);

  const role = getRole();
  if (role !== 'admin') {
    return (
      <div className="admin-container">
        <h2>Access Denied</h2>
        <p style={{ color: '#e74c3c' }}>You do not have admin privileges.</p>
      </div>
    );
  }

  const handleAddProduct = () => {
    axios.post('http://localhost:5050/api/products', { name, description: desc, price }, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }).then(() => {
      setName('');
      setDesc('');
      setPrice('');
      window.location.reload();
    });
  };

  const handleDelete = (id) => {
    axios.delete(`http://localhost:5050/api/products/${id}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }).then(() => window.location.reload());
  };

  const startEdit = (product) => {
    setEditing(product.id);
    setEditData({ name: product.name, description: product.description, price: product.price });
  };

  const handleEdit = (id) => {
    axios.put(`http://localhost:5050/api/products/${id}`, editData, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }).then(() => {
      setEditing(null);
      window.location.reload();
    });
  };

  return (
    <div className="admin-container">
      <h2>Admin Panel</h2>
      <input type="text" placeholder="Product Name" value={name} onChange={e => setName(e.target.value)} />
      <input type="text" placeholder="Description" value={desc} onChange={e => setDesc(e.target.value)} />
      <input type="number" placeholder="Price" value={price} onChange={e => setPrice(e.target.value)} />
      <button onClick={handleAddProduct}>Add Product</button>
      <h3>Products</h3>
      <ul>
        {products.map(product => (
          <li key={product.id}>
            {editing === product.id ? (
              <>
                <input value={editData.name} onChange={e => setEditData({ ...editData, name: e.target.value })} />
                <input value={editData.description} onChange={e => setEditData({ ...editData, description: e.target.value })} />
                <input value={editData.price} type="number" onChange={e => setEditData({ ...editData, price: e.target.value })} />
                <button onClick={() => handleEdit(product.id)}>Save</button>
                <button onClick={() => setEditing(null)}>Cancel</button>
              </>
            ) : (
              <>
                {product.name} - ₹{product.price}
                <button onClick={() => startEdit(product)}>Edit</button>
                <button onClick={() => handleDelete(product.id)}>Delete</button>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Admin;