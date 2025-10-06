import React from 'react';
import './Dice.css';

const Dice = ({ onRoll, roll }) => {
  return (
    <div className="dice-container">
      <button onClick={onRoll}>Roll Dice</button>
      {roll && <div className="dice-roll">🎲 Rolled: {roll}</div>}
    </div>
  );
};

export default Dice;
 