import React, { useState } from 'react';
import './LoginPage.css';

const LoginPage = ({ onStartGame }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  function handleLogin() {
    if (!username || !password) {
      alert('Please enter username and password');
      return;
    }

    setLoading(true);
    
    fetch('https://snakes-and-ladders-3-0.onrender.com/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    .then(response => response.json().then(data => ({ response, data })))
    .then(({ response, data }) => {
      if (response.ok) {
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('username', data.username);
        alert('Login successful!');
        onStartGame();
      } else {
        alert('Login failed: ' + data.error);
      }
    })
    .catch(error => {
      alert('Error: Cannot connect to server');
    })
    .finally(() => {
      setLoading(false);
    });
  }

  function handleRegister() {
    if (!username || !password) {
      alert('Please enter username and password');
      return;
    }

    setLoading(true);
    
    fetch('https://snakes-and-ladders-3-0.onrender.com/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    .then(response => response.json().then(data => ({ response, data })))
    .then(({ response, data }) => {
      if (response.ok) {
        alert('Account created! Now you can login.');
      } else {
        alert('Create account failed: ' + data.error);
      }
    })
    .catch(error => {
      alert('Error: Cannot connect to server');
    })
    .finally(() => {
      setLoading(false);
    });
  }

  return (
    <div className="login-page">
      <div className="login-container">
        <h1> Snakes and Ladders</h1>
        
        
        <div className="login-form">
          <h2>Login to Play</h2>
          
          <input 
            type="text" 
            placeholder="Enter your username" 
            value={username}
            onChange={(e) => setUsername(e.target.value)}

          />
          
          <input
            type="password" 
            placeholder="Enter your password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}

          />
          
          <button onClick={handleLogin} disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
          
          <button onClick={handleRegister} disabled={loading} style={{marginTop: '10px', backgroundColor: '#28a745'}}>
            {loading ? 'Creating account...' : 'Create New Account'}
          </button>
        </div>
        
        <div className="how-to-play">
          <h2>How to Play</h2>
          <p> Roll dice →  Move →  Ladders up →  Snakes down →  Reach 100!</p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;