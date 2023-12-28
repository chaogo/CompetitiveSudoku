import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SignupLogin from "./SignupLogin";
import PlayModeChoice from "./PlayModeChoice";
import GameRoomChoice from "./GameRoomChoice";
import DifficultyChoice from "./DifficultyChoice";
import SudokuBoard from "./SudokuBoard";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SignupLogin />} />
        <Route path="/play-mode" element={<PlayModeChoice />} />
        <Route path="/game-room" element={<GameRoomChoice />} />
        <Route path="/difficulty" element={<DifficultyChoice />} />
        <Route path="/sudoku-board" element={<SudokuBoard />} />
      </Routes>
    </Router>
  );
};

export default App;
