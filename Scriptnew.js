const express = require("express");
const mysql = require("mysql2");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json());
app.use(cors());

// Database Connection
const db = mysql.createConnection({
  host: "localhost",      // Replace with your DB host
  user: "root",           // Replace with your DB username
  password: "password",   // Replace with your DB password
  database: "mydb"        // Replace with your DB name
});

// Connect to Database
db.connect((err) => {
  if (err) {
    console.error("Database connection failed:", err);
  } else {
    console.log("Connected to the database.");
  }
});

// API to run SELECT query
app.get("/api/get-data", (req, res) => {
  const query = "SELECT * FROM my_table"; // Replace with your table name

  db.query(query, (err, results) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.json(results);
    }
  });
});

// Start the Server
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
