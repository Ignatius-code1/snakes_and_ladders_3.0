import React, { useState, useEffect } from 'react';

function App() {
  const [gameState, setGameState] = useState(null);

  const fetchGameState = async () => {
    try {
      const response = await fetch('http://localhost:5000/game-state');
      const data = await response.json();
      setGameState(data);
    } catch (error) {
      console.log('Backend not ready');
    }
  };

  const startGame = async () => {
    await fetch('http://localhost:5000/start-game', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ players: ['Player 1', 'Player 2'] })
    });
    fetchGameState();
  };

  const rollDice = async () => {
    await fetch('http://localhost:5000/roll-dice', { method: 'POST' });
    fetchGameState();
  };

  useEffect(() => {
    fetchGameState();
  }, []);

  const renderBoard = () => {
    const squares = [];
    for (let i = 100; i >= 1; i--) {
      const row = Math.floor((i - 1) / 10);
      const isReverse = row % 2 === 1;
      const position = isReverse ? 100 - i + 1 : i;
      
      const playersHere = gameState ? 
        Object.entries(gameState.positions).filter(([player, pos]) => pos === position).map(([player]) => player) : [];
      
      squares.push(
        <div key={i} style={{ 
          width: '40px', 
          height: '40px', 
          border: '1px solid black',
          display: 'inline-block',
          textAlign: 'center',
          lineHeight: '20px',
          fontSize: '10px',
          position: 'relative'
        }}>
          {position}
          {playersHere.map(player => 
            <div key={player} style={{color: 'red', fontWeight: 'bold'}}>{player[0]}</div>
          )}
        </div>
      );
      
      if (i % 10 === 1) squares.push(<br key={`br-${i}`} />);
    }
    return squares;
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h1>Snakes and Ladders</h1>
      <button onClick={startGame}>Start Game</button>
      <button onClick={rollDice}>Roll Dice</button>
      <div style={{ marginTop: '20px' }}>
        {renderBoard()}
      </div>
      {gameState && (
        <div>
          <p>Current Player: {gameState.currentPlayer}</p>
          <p>Positions: {JSON.stringify(gameState.positions)}</p>
        </div>
      )}
    </div>
  );
}

export default App;