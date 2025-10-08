import React, { useState } from 'react';
import './LoginPage.css';

const LoginPage = ({ onStartGame }) => {
  // User type storage using usestate
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  // Login function for the user/player to the game
  function handleLogin() {
    if (!username || !password) {
      alert('Please enter username and password');
      return;
    }

    setLoading(true);
    
    // The front end sends a POST request to the backend Flask server to get the token 
    // for authentication of username and password
    fetch('https://https://snakes-and-ladders-3-0.onrender.com/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }, 
      // this tells the server to expect json data for flask to process
      body: JSON.stringify({ username, password })
      // this makes the data shared to the server to bcm a json format
    })
    .then(response => {
      // Get both response and data together
      return response.json().then(data => ({ response, data }));
    })
    .then(({ response, data }) => {
      // checks if response was successful to allow login by user/player
      if (response.ok) {
        // this saves token gotten for user/player for later use
        // This is also where the JWT is received and stored.
        localStorage.setItem('token', data.access_token);  
        localStorage.setItem('username', data.username);
        alert('Login successful!');
        
        onStartGame();
      } else {
        alert('Login failed: ' + data.error);
      }
    })
    .catch(error => {
      // helps handle network errors
      alert('Error: Cannot connect to server');
    })
    .finally(() => {
      // stops loading, whether success or error
      setLoading(false);
    });
  }

  // Create new account function for the user/player 
  function handleRegister() {
    if (!username || !password) {
      alert('Please enter username and password');
      return;
    }

    setLoading(true);
    
    // Flask server creates or stores new account
    fetch('https://YOUR-RENDER-URL.onrender.com/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    .then(response => {
      // Get both response and data together
      return response.json().then(data => ({ response, data }));
    })
    .then(({ response, data }) => {
      // Checks if registration was successful
      if (response.ok) {
        alert('Account created! Now you can login.');
      } else {
        alert('Create account failed: ' + data.error);
      }
    })
    .catch(error => {
      // helps to andle network errors
      alert('Error: Cannot connect to server');
    })
    .finally(() => {
      // this stops the loading, whether success or error
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
            //onchange helps to update the state as user types in the username
          />
          
          <input
            type="password" 
            placeholder="Enter your password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            //onchange helps to update the state as user types in the password
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