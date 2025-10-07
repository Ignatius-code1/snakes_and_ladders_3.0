import React from 'react';
import './Board.css';

const Board = ({ positions, snakes, ladders, BOARD_SIZE }) => {
  const renderBoard = () => {
    const board = [];
    let cellNum = BOARD_SIZE;

    for (let row = 0; row < 10; row++) {
      const rowCells = [];
      const isOddRow = row % 2 === 1;
      const start = cellNum - 9;
      const end = cellNum;
      const nums = isOddRow
        ? Array.from({ length: 10 }, (_, i) => start + i) // left-to-right
        : Array.from({ length: 10 }, (_, i) => end - i);  // right-to-left

      nums.forEach((num) => {
        rowCells.push(
          <div
            key={num}
            className={`cell ${snakes[num] ? 'snake' : ''} ${ladders[num] ? 'ladder' : ''}`}
          >
            {num}
            <div className="players">
              {positions.player1 === num && <div className="player player1">P1</div>}
              {positions.player2 === num && <div className="player player2">P2</div>}
            </div>
          </div>
        );
      });
      board.push(
        <div key={row} className="board-row">
          {rowCells}
        </div>
      );
      cellNum -= 10;
    }
    return board;
  };

  return (
    <div className="board">
      {renderBoard()}
    </div>
  );
};

export default Board;
