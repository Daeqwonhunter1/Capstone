// const express = require("express");
// const app = express();
// const http = require("http");
// const { Server } = require("socket.io");
const cors = require("cors");
// const { exit } = require("process");
// const spawner = require("child_process").spawn;
// const net = require("net");

const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const net = require("net");

const app = express();

app.use(cors());

const server = http.createServer(app);

const io = new Server(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"],
  },
});

io.on("connection", (socket) => {
  console.log(`User Connected: ${socket.id}`);

  // Send data to Python server
  socket.on("Send_Message", (socketData) => {
    console.log("Data to pass", socketData);

    // Create a TCP client and connect to the Python server
    const pythonClient = net.createConnection(
      { port: 3002, host: "127.0.0.1" },
      () => {
        console.log("Connected to Python script");

        // Send data to the Python script
        pythonClient.write(JSON.stringify(socketData));
        pythonClient.on("data", (data) => {
          const responseString = data.toString("utf-8");
          console.log("Data received from Python script: ", responseString);

          io.emit("Received_Message", { response: responseString });
        });
        pythonClient.end();
      }
    );
  });
});

server.listen(3001, () => {
  console.log("SERVER IS RUNNING");
});
