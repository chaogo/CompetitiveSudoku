import React from "react";
import { useNavigate } from "react-router-dom";

const PlayModeChoice = () => {
  let navigate = useNavigate();

  const handlePlayerMode = () => {
    navigate("/game-room"); // Navigate to game room choice page
  };

  const handleAIMode = () => {
    navigate("/difficulty"); // Navigate to difficulty choice page
  };

  return (
    <div>
      <h2>Choose Play Mode</h2>
      <button onClick={handlePlayerMode}>Play with Other Player</button>
      <button onClick={handleAIMode}>Play with AI</button>
      <button>Watch Ongoing Games</button>
    </div>
  );
};

export default PlayModeChoice;
