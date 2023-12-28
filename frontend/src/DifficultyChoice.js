import React from "react";
import { useNavigate } from "react-router-dom";

const DifficultyChoice = () => {
  let navigate = useNavigate();

  const handleDifficultySelection = (difficulty) => {
    // Navigate to SudokuBoard with difficulty in the state
    navigate("/sudoku-board", { state: { difficulty } });
  };

  return (
    <div>
      <h2>Choose Difficulty</h2>
      <button onClick={() => handleDifficultySelection("easy")}>Easy</button>
      <button onClick={() => handleDifficultySelection("medium")}>
        Medium
      </button>
      <button onClick={() => handleDifficultySelection("hard")}>Hard</button>
      <button onClick={() => handleDifficultySelection("expert")}>
        Expert
      </button>
    </div>
  );
};

export default DifficultyChoice;
