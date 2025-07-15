const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const routes = require('./routes');
const db = require('./db');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5050;

app.use(cors());
app.use(express.json());

app.get('/test', (req, res) => res.send('👋 Express is working')); // ✅ debug route

app.use('/api', routes); // ✅ connect routers

// ✅ No need to call db.connect() again
app.listen(PORT,'0.0.0.0', () => {
  console.log('✅ Connected to MySQL!');
  console.log(`🚀 Backend running on port ${PORT}`);
});