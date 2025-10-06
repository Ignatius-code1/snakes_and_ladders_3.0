import React, { useState } from 'react';
import { createRoot } from '@react-dom/client';
import App from './components/App.jsx';
import './index.css';

const root = createRoot(document.getElementById('root'));
root.render(
  <StrictMode strictMode>
    <App />
  </StrictMode>
);