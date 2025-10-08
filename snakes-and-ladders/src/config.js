// API Configuration
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://YOUR-RENDER-URL.onrender.com'  // Replace with your actual Render URL
  : 'http://localhost:5001';

export { API_BASE_URL };