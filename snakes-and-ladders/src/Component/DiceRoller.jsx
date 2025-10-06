import React, { useState } from 'react';
import './DiceRoller.css';

const DiceRoller = ({ onRoll, disabled }) => {
  const [rolling, setRolling] = useState(false);
  const [diceValue, setDiceValue] = useState(1);

  const rollDice = () => {
    if (disabled || rolling) return;
    
    setRolling(true);
    
    let rolls = 0;
    const interval = setInterval(() => {
      setDiceValue(Math.floor(Math.random() * 6) + 1);
      rolls++;
      
      if (rolls > 15) {
        clearInterval(interval);
        const finalValue = Math.floor(Math.random() * 6) + 1;
        setDiceValue(finalValue);
        setRolling(false);
        onRoll(finalValue);
      }
    }, 100);
  };

  return (
    <div className="dice-roller">
      <div 
        className={`dice ${rolling ? 'rolling' : ''}`} 
        aria-live="polite"
        aria-label={`Dice shows ${diceValue}`}
      >
        {diceValue}
      </div>
      <button 
        onClick={rollDice} 
        disabled={disabled || rolling}
        className="roll-button"
        aria-label={rolling ? 'Dice is rolling' : 'Roll the dice'}
      >
        {rolling ? 'Rolling...' : 'Roll Dice'}
      </button>
    </div>
  );
};

export default DiceRoller;