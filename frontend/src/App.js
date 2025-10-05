import React, { useState, useEffect } from 'react';
import './App.css';
import boardImage from './assets/Board.jpeg';

function App() {
  const [gameState, setGameState] = useState(null);
  const [diceRoll, setDiceRoll] = useState(null);

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
    const response = await fetch('http://localhost:5000/roll-dice', { method: 'POST' });
    const data = await response.json();
    setDiceRoll(data.dice);
    fetchGameState();
  };

  useEffect(() => {
    fetchGameState();
  }, []);

  const getPositionStyle = (cellNumber) => {
    const row = Math.floor((cellNumber - 1) / 10);
    const col = (cellNumber - 1) % 10;
    const displayRow = 10 - 1 - row;
    const displayCol = row % 2 === 0 ? col : 10 - 1 - col;
    
    return {
      position: 'absolute',
      left: `${(displayCol * 10) + 5}%`,
      top: `${(displayRow * 10) + 5}%`,
      transform: 'translate(-50%, -50%)'
    };
  };

  return (
    <div className="App">
      <h1>Snakes and Ladders</h1>
      <button onClick={startGame}>Start Game</button>
      <button onClick={rollDice}>Roll Dice</button>
      {diceRoll && <div>Rolled: {diceRoll}</div>}
      
      {gameState && (
        <div className="game-board">
          <img src={boardImage} alt="Snakes and Ladders Board" className="board-image" />
          {Object.entries(gameState.positions).map(([player, position], index) => (
            <div 
              key={player}
              className="player-token"
              style={{
                ...getPositionStyle(position || 1),
                backgroundColor: index === 0 ? '#FF6B6B' : '#4ECDC4'
              }}
              title={`${player} - Position: ${position}`}
            ></div>
          ))}
        </div>
      )}
      
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