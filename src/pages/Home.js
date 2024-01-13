import React, { useEffect, useState } from "react";
import { loadUsers } from "../components/Users";
import Navbar from "../layout/Navbar";
import { io } from "socket.io-client";

const socket = io.connect("http://localhost:3001");

export default function Home() {
  // const [users, setUsers] = useState([]);
  const [state, setState] = useState({
    val: "",
  });

  const sendMessage = (e) => {
    e.preventDefault();
    console.log(state.val);
    socket.emit("Send_Message", state.val);
  };

  useEffect(() => {
    socket.on("Received_Message", (data) => {
      alert(data.toString());
    });
  }, [socket]);

  const handleChange = (e) => {
    console.log(e.target.value);
    setState({ val: e.target.value });
  };

  return (
    <div id="container">
      {/* If signed in show navbar */}
      <div className="custom-input-container">
    
        <form onSubmit={(e) => sendMessage(e)}>
          <input
            type="text"
            className="form-control custom-input"
            placeholder="Movie"
            aria-label="Movie"
            aria-describedby="addon-wrapping"
            value={state.val}
            onChange={(e) => handleChange(e)}
          />
          <button className="custom-button">Click</button>{" "}
          {/* Add a custom class for styling */}
        </form>
      </div>
    </div>
  );
}
