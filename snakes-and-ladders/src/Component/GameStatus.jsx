import React, { useState } from 'react';
import './GameStatus.css';

const GameStatus = ({ message }) => {
  return (
    <div className="game-status" role="status" aria-live="polite">
      <p>{message}</p>
    </div>
  );
};

export default GameStatus;