import React, { useState } from 'react';
import './App.css';
import GameBoard from './Component/GameBoard';
import DiceRoller from './Component/DiceRoller';
import GameStatus from './Component/GameStatus';

import LoginPage from './Component/LoginPage';

const App = () => {
  const BOARD_SIZE = 100;
  
  const snakes = {
    16: 6,
    46: 25,
    49: 11,
    62: 19,
    64: 60,
    74: 53,
    89: 68,
    92: 88,
    95: 75,
    99: 80,
  };
  
  const ladders = {
    2: 38,
    7: 14,
    8: 31,
    15: 26,
    28: 84,
    36: 44,
    51: 67,
    78: 98,
    87: 94,
  };

  const [positions, setPositions] = useState({ player1: 1, player2: 1 });
  const [currentPlayer, setCurrentPlayer] = useState(1);
  const [gameMessage, setGameMessage] = useState("");
  const [winner, setWinner] = useState(null);
  const [rolling, setRolling] = useState(false);
  const [gameStarted, setGameStarted] = useState(false);

  const handleDiceRoll = (roll) => {
    if (winner || rolling) return;
    setRolling(true);

    const playerKey = `player${currentPlayer}`;
    let newPosition = positions[playerKey] + roll;

    if (newPosition > BOARD_SIZE) {
      setCurrentPlayer(currentPlayer === 1 ? 2 : 1);
      setRolling(false);
      return;
    }

    if (newPosition === BOARD_SIZE) {
      setPositions((prev) => ({ ...prev, [playerKey]: newPosition }));
      setWinner(currentPlayer);
      setGameMessage(`🎉 Player ${currentPlayer} wins! 🏆`);
      setRolling(false);
      return;
    }

    if (ladders[newPosition]) {
      newPosition = ladders[newPosition];
    } else if (snakes[newPosition]) {
      newPosition = snakes[newPosition];
    }

    setPositions((prev) => ({
      ...prev,
      [playerKey]: newPosition
    }));

    if (roll !== 6) {
      setCurrentPlayer(currentPlayer === 1 ? 2 : 1);
    }
    setRolling(false);
  };

  const resetGame = () => {
    setPositions({ player1: 1, player2: 1 });
    setCurrentPlayer(1);
    setGameMessage("");
    setWinner(null);
    setRolling(false);
  };

  const startGame = () => {
    setGameStarted(true);
  };

  const backToLogin = () => {
    setGameStarted(false);
    resetGame();
  };

  if (!gameStarted) {
    return <LoginPage onStartGame={startGame} />;
  }

  return (
    <div className="app">
      <header>
        <h1>🐍 Snakes and Ladders</h1>
        <button 
          className="back-button"
          onClick={backToLogin}
          aria-label="Back to main menu"
        >
          🏠 Main Menu
        </button>
      </header>
      
      <div className="game-container">
        <div className="board-section">
          <GameBoard
            playersPositions={positions}
            snakes={snakes}
            ladders={ladders}
            currentPlayer={currentPlayer}
          />
          <GameStatus message={gameMessage} />
          <DiceRoller onRoll={handleDiceRoll} disabled={!!winner || rolling} />
          <button
            className="reset-button"
            onClick={resetGame}
            aria-label="Reset the game"
          >
            🔄 Reset Game
          </button>
        </div>
      </div>
      
      {winner && (
        <div className="game-over-modal" role="dialog" aria-labelledby="winner-title">
          <div className="winner-card">
            <h2 id="winner-title">Game Over!</h2>
            <div className="winner-info">
              <div
                className="winner-token"
                style={{ backgroundColor: winner === 1 ? '#FF6B6B' : '#4ECDC4' }}
                aria-hidden="true"
              ></div>
              <h3>Player {winner} Wins!</h3>
            </div>
            <button
              className="play-again-button"
              onClick={resetGame}
              aria-label="Play again"
            >
              Play Again
            </button>
          </div>
        </div>
      )}
      
      <div className="legend" aria-label="Game legend">
        <div><span className="legend-snake"></span> Snake</div>
        <div><span className="legend-ladder"></span> Ladder</div>
      </div>

    </div>
  );
};

export default App;