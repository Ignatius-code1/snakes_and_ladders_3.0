import React, { useState, useEffect } from 'react';

const Games = () => {
  const [games, setGames] = useState([]);

  // Get all games when page loads
  useEffect(() => {
    fetch('http://localhost:5001/games')
      .then(response => response.json())
      .then(data => setGames(data))
      .catch(error => console.log('Error:', error));
  }, []);

  return (
    <div style={{padding: '20px'}}>
      <h1>🎮 Games Page</h1>
      <p>Here are all the games:</p>
      
      {games.length === 0 ? (
        <p>No games yet. Create one!</p>
      ) : (
        <ul>
          {games.map(game => (
            <li key={game.id}>
              Game #{game.id} - Status: {game.status}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Games;