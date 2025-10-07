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

  const [positions, setPositions] = useState({ player1: 1, luna: 1 });
  const [currentPlayer, setCurrentPlayer] = useState(1);
  const [gameMessage, setGameMessage] = useState("");
  const [winner, setWinner] = useState(null);
  const [rolling, setRolling] = useState(false);
  const [gameStarted, setGameStarted] = useState(false);
  const [moveComments, setMoveComments] = useState([]);

  const makeMove = (player, roll) => {
    const playerKey = player === 1 ? 'player1' : 'luna';
    const playerName = player === 1 ? 'You' : 'Luna';
    let newPosition = positions[playerKey] + roll;
    let comment = `${playerName} rolled ${roll}!`;

    if (newPosition > BOARD_SIZE) {
      comment += ` Can't move past 100.`;
      addComment(comment);
      return false;
    }

    if (newPosition === BOARD_SIZE) {
      setPositions((prev) => ({ ...prev, [playerKey]: newPosition }));
      setWinner(player);
      comment += ` Reached 100 and wins! `;
      setGameMessage(` ${playerName} wins! `);
      addComment(comment);
      return true;
    }

    if (ladders[newPosition]) {
      const ladderEnd = ladders[newPosition];
      newPosition = ladderEnd;
      comment += ` Climbed ladder to ${ladderEnd}! 🪜`;
    } else if (snakes[newPosition]) {
      const snakeEnd = snakes[newPosition];
      newPosition = snakeEnd;
      comment += ` Hit snake, slid down to ${snakeEnd}! `;
    } else {
      comment += ` Moved to ${newPosition}.`;
    }

    setPositions((prev) => ({
      ...prev,
      [playerKey]: newPosition
    }));

    addComment(comment);
    return roll === 6;
  };

  const addComment = (comment) => {
    setMoveComments(prev => [comment, ...prev.slice(0, 4)]);
  };

  const handleDiceRoll = (roll) => {
    if (winner || rolling) return;
    setRolling(true);

    const keepTurn = makeMove(currentPlayer, roll);
    
    setTimeout(() => {
      if (!keepTurn && !winner) {
        setCurrentPlayer(currentPlayer === 1 ? 2 : 1);
        
        // Luna's turn
        if (currentPlayer === 1) {
          setTimeout(() => {
            const lunaRoll = Math.floor(Math.random() * 6) + 1;
            const lunaKeepTurn = makeMove(2, lunaRoll);
            if (!lunaKeepTurn && !winner) {
              setCurrentPlayer(1);
            }
            setRolling(false);
          }, 1500);
        } else {
          setRolling(false);
        }
      } else {
        setRolling(false);
      }
    }, 500);
  };

  const resetGame = () => {
    setPositions({ player1: 1, luna: 1 });
    setCurrentPlayer(1);
    setGameMessage("");
    setWinner(null);
    setRolling(false);
    setMoveComments([]);
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
              <h3>{winner === 1 ? 'You Win!' : 'Luna Wins!'}</h3>
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
      
      <div className="game-info">
        <div className="players-info">
          <div className="player-info">
            <span className="player-token" style={{backgroundColor: '#FF6B6B'}}></span>
            <span>You (Position: {positions.player1})</span>
          </div>
          <div className="player-info">
            <span className="player-token" style={{backgroundColor: '#4ECDC4'}}></span>
            <span>Luna (Position: {positions.luna})</span>
          </div>
        </div>
        
        <div className="move-comments">
          <h3>Recent Moves:</h3>
          {moveComments.map((comment, index) => (
            <div key={index} className="comment">{comment}</div>
          ))}
        </div>
        
        <div className="legend" aria-label="Game legend">
          <div><span className="legend-snake"></span> Snake</div>
          <div><span className="legend-ladder"></span> Ladder</div>
        </div>
      </div>

    </div>
  );
};

export default App;