import React from "react";
import { useNavigate } from "react-router-dom";

const SignupLogin = () => {
  let navigate = useNavigate();

  const handleEnterGame = () => {
    navigate("/play-mode"); // Navigate to play mode choice page
  };

  return (
    <div>
      <h2>Sign Up / Login</h2>
      <button onClick={handleEnterGame}>Enter Game</button>
    </div>
  );
};

export default SignupLogin;
