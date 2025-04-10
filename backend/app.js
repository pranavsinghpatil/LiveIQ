// app.js

const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const bodyParser = require('body-parser');

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ extended: true, limit: '50mb' }));

// Routes
const fileUploadRoutes = require('./routes/fileUpload');
const linkImporterRoutes = require('./routes/linkImporter');
const authRoutes = require('./routes/auth');
const hybridRoutes = require('./routes/hybridBuilder');
const chatRoutes = require('./routes/chatResponder');

// Mount Routes
app.use('/api/upload', fileUploadRoutes);
app.use('/api/process', linkImporterRoutes);
app.use('/api/auth', authRoutes);
app.use('/api/hybrid', hybridRoutes);
app.use('/api/chat', chatRoutes);

// Health Check
app.get('/', (req, res) => {
  res.send('VoxStitch backend is running ✅');
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});


// 🧩 Part	      ✅ Purpose
// cors()	      Allow frontend (on a different port or domain) to communicate with this backend
// body-parser	  Parse JSON and file payloads (PDF, audio, etc.)
// dotenv	      Load API keys and Supabase credentials from .env
// /api/upload	  For file uploads (PDFs, images, videos, etc.)
// /api/process	  For processing shared links (YouTube, ChatGPT, etc.)
// /api/auth	  Supabase-based auth system (signup/login/session)
// /api/hybrid	  Creating & managing merged/hybrid chats
// /api/chat	  Sending chat messages to the selected LLM