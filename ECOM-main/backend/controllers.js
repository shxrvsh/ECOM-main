const db = require('./db');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET;

// === AUTH ===
exports.register = (req, res) => {
  const { name, email, password } = req.body;
  const hashed = bcrypt.hashSync(password, 10);
  db.query('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', [name, email, hashed],
    (err, result) => {
      if (err) return res.status(500).json({ error: err });
      res.json({ message: 'User registered successfully' });
    });
};

exports.login = (req, res) => {
  const { email, password } = req.body;
  db.query('SELECT * FROM users WHERE email = ?', [email], (err, users) => {
    if (err || users.length === 0) return res.status(401).json({ error: 'Invalid credentials' });

    const user = users[0];
    const isMatch = bcrypt.compareSync(password, user.password);
    if (!isMatch) return res.status(401).json({ error: 'Invalid credentials' });

    const token = jwt.sign({ id: user.id, role: user.role }, JWT_SECRET, { expiresIn: '1h' });
    res.json({ token, user: { id: user.id, name: user.name, role: user.role } });
  });
};

// === PRODUCTS ===
exports.getProducts = (req, res) => {
  db.query('SELECT * FROM products', (err, results) => {
    if (err) {
      console.error('❌ MySQL error:', err);
      return res.status(500).json({ error: err });
    }
    console.log('✅ products returned:', results.length);
    res.json(results);
  });
};

exports.addProduct = (req, res) => {
  const { name, description, price, image } = req.body;
  db.query('INSERT INTO products (name, description, price, image) VALUES (?, ?, ?, ?)',
    [name, description, price, image],
    (err, result) => {
      if (err) return res.status(500).json({ error: err });
      res.json({ message: 'Product added', productId: result.insertId });
    });
};

exports.deleteProduct = (req, res) => {
  const { id } = req.params;
  db.query('DELETE FROM products WHERE id = ?', [id], (err) => {
    if (err) return res.status(500).json({ error: err });
    res.json({ message: 'Product deleted' });
  });
};

exports.editProduct = (req, res) => {
  const { id } = req.params;
  const { name, description, price } = req.body;
  db.query('UPDATE products SET name=?, description=?, price=? WHERE id=?',
    [name, description, price, id],
    (err) => {
      if (err) return res.status(500).json({ error: err });
      res.json({ message: 'Product updated' });
    });
};

// === CART ===
exports.addToCart = (req, res) => {
  const { user_id, product_id, quantity } = req.body;
  db.query('INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)',
    [user_id, product_id, quantity],
    (err) => {
      if (err) return res.status(500).json({ error: err });
      res.json({ message: 'Item added to cart' });
    });
};

exports.getCart = (req, res) => {
  const userId = req.params.userId;
  db.query(
    `SELECT c.id, p.name, p.price, c.quantity
     FROM cart c
     JOIN products p ON c.product_id = p.id
     WHERE c.user_id = ?`,
    [userId],
    (err, results) => {
      if (err) return res.status(500).json({ error: err });
      res.json(results);
    }
  );
};

exports.removeFromCart = (req, res) => {
  const { id } = req.params;
  db.query('DELETE FROM cart WHERE id = ?', [id], (err) => {
    if (err) return res.status(500).json({ error: err });
    res.json({ message: 'Item removed from cart' });
  });
};

exports.clearCart = (req, res) => {
  const userId = req.params.userId;
  db.query('DELETE FROM cart WHERE user_id = ?', [userId], (err) => {
    if (err) return res.status(500).json({ error: err });
    res.json({ message: 'Cart cleared' });
  });
};