import React, { useState, useEffect } from "react";
import axios from "axios";

const SudokuBoard = () => {
  const [selectedCell, setSelectedCell] = useState(null);
  const [board, setBoard] = useState([]);

  useEffect(() => {
    // asynchronous
    // Fetch the initial game state from the backend when the component mounts
    axios
      .get("http://127.0.0.1:8000/api/get-game-board")
      .then((response) => {
        setBoard(response.data.game_board);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, []);

  // If the board is still an empty array, render a loading message
  if (!board) {
    return <div>Loading...</div>;
  }

  const handleCellClick = (row, col) => {
    setSelectedCell({ row, col });
  };

  const handleNumberInput = (e) => {
    const { value } = e.target;
    const updatedBoard = [...board];
    const { row, col } = selectedCell;
    updatedBoard[row][col] = parseInt(value);
    setBoard(updatedBoard);
  };

  const handleSubmitMove = () => {
    const { row, col } = selectedCell;
    const number = board[row][col];

    // Send an HTTP POST request to the backend with the selected cell's coordinates and the entered number
    axios
      .post("/api/make-move", { row, col, number })
      .then((response) => {
        // Once you receive a response from the backend, update the board with the new game state
        const updatedBoard = response.data.game_board;
        setBoard(updatedBoard);

        // Clear the selectedCell state
        setSelectedCell(null);
      })
      .catch((error) => {
        // Handle any error that occurred during the request
        console.error("Error:", error);
      });
  };

  return (
    <div style={{ display: "inline-block", margin: "20px" }}>
      {board.map((row, rowIndex) => (
        <div key={rowIndex} style={{ display: "flex" }}>
          {row.map((cell, colIndex) => (
            <div
              key={colIndex}
              style={{
                width: "50px",
                height: "50px",
                border: "1px solid black",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                fontSize: "1.2rem",
                fontWeight: "bold",
                backgroundColor: cell !== 0 ? "#f0f0f0" : "#ffffff",
                color: cell !== 0 ? "#333333" : "#000000",
              }}
              onClick={() => handleCellClick(rowIndex, colIndex)}
            >
              {cell !== 0 ? cell : ""}
            </div>
          ))}
        </div>
      ))}
      <button
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          fontSize: "1rem",
          backgroundColor: "#007bff",
          color: "#ffffff",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
        onClick={handleSubmitMove}
      >
        Submit Move
      </button>
    </div>
  );
};

export default SudokuBoard;
