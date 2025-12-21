import React from 'react';
import ReactDOM from 'react-dom/client';
import './App.css';
import App from './App';

/**
 * SEMANTIC: React application entry point
 * Mount React application to DOM root element
 */
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
