import React, { useState, useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";

const SudokuBoard = () => {
  const [selectedCell, setSelectedCell] = useState(null);
  const [board, setBoard] = useState([]);
  const [message, setMessage] = useState("");
  const ws = useRef(null);

  // Use useLocation to access the state passed from DifficultyChoice
  const location = useLocation();

  useEffect(() => {
    const difficulty = location.state?.difficulty;
    console.log("Selected Difficulty:", difficulty);

    ws.current = new WebSocket("ws://127.0.0.1:8000/ws/sudoku/15/");
    // Listen for messages
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.message) {
        setMessage(data.message);
      }
      if (data.game_board) {
        // Split the entire string by newlines
        const allLines = data.game_board.trim().split("\n");

        // Extract the first line for height and width information
        const [height, width] = allLines[0].trim().split(/\s+/).map(Number);

        // Process the remaining lines as the board
        const board = allLines.slice(1).map((row) =>
          row
            .trim()
            .split(/\s+/)
            .map((cell) => (cell === "." ? "0" : cell))
        );
        setBoard(board);
      }
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket Error:", error);
    };

    ws.current.onclose = () => {
      console.log("WebSocket connection closed");
    };

    return () => {
      if (ws.current) {
        console.log("Cleaning up WebSocket");
        // ws.current.close(); // need fix
      }
    };
  }, []);

  if (!board) {
    return <div>Loading...</div>;
  }

  const handleCellClick = (row, col) => {
    setSelectedCell({ row, col });
  };

  const handleNumberInput = (e) => {
    const { value } = e.target;
    if (selectedCell) {
      const updatedBoard = [...board];
      const { row, col } = selectedCell;
      updatedBoard[row][col] = parseInt(value);
      setBoard(updatedBoard);
    }
  };

  const handleSubmitMove = () => {
    if (selectedCell && ws.current) {
      const { row, col } = selectedCell;
      const number = board[row][col];

      // Structure the data as required by the server
      const moveData = {
        action: "move",
        move: {
          i: row,
          j: col,
          value: number,
        },
      };

      // Send the structured data as a JSON string
      ws.current.send(JSON.stringify(moveData));
    }
  };

  return (
    <div style={{ display: "inline-block", margin: "20px" }}>
      {board.map((row, rowIndex) => (
        <div key={rowIndex} style={{ display: "flex" }}>
          {row.map((cell, colIndex) => (
            <input
              type="number"
              min="1"
              max="9"
              key={colIndex}
              value={cell !== "0" ? cell : ""}
              readOnly={cell !== "0"}
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
              onChange={handleNumberInput}
            />
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
      <div style={{ marginTop: "20px" }}>
        <strong>Messages:</strong>
        <div>{message}</div>
      </div>
    </div>
  );
};

export default SudokuBoard;
