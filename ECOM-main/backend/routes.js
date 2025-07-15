const express = require('express');
const router = express.Router();
const controller = require('./controllers');
const jwt = require('jsonwebtoken');

// Auth routes
router.post('/login', controller.login);
router.post('/register', controller.register);

// Middleware to authenticate token
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) return res.sendStatus(401);

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}

// Middleware to require admin role
function requireAdmin(req, res, next) {
  if (req.user.role !== 'admin') return res.sendStatus(403);
  next();
}

// Product routes
router.get('/products', controller.getProducts);
router.post('/products', authenticateToken, requireAdmin, controller.addProduct); // Admin only
router.put('/products/:id', authenticateToken, requireAdmin, controller.editProduct);
router.delete('/products/:id', authenticateToken, requireAdmin, controller.deleteProduct); // Admin only

// Cart routes
router.post('/cart', authenticateToken, controller.addToCart); // Require login
router.get('/cart/:userId', authenticateToken, controller.getCart); // Require login
router.delete('/cart/:id', authenticateToken, controller.removeFromCart);
router.delete('/cart/user/:userId', authenticateToken, controller.clearCart);

module.exports = router;