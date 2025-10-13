import express from "express";
import mongoose from "mongoose";
import dotenv from "dotenv";
import cors from "cors"; 
import bcrypt from "bcrypt";
import User from "./models/User.js";

dotenv.config();


// setting up the app to read data from a form
const app = express();
app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// connect to MongoDB
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log("✅ Connected to MongoDB"))
  .catch(err => console.error("❌ MongoDB connection error:", err));

// checking backend 
app.get("/", (req, res) => res.send("Backend running!"));


// Route to handle user registration
app.post("/register", async (req, res) => {
  try {
    const { NetID, email, username, password } = req.body;

    // check required fields
    if (!NetID || !email || !username || !password) {
      return res.status(400).json({ error: "All fields are required." });
    }

    //normalize inputs
    const normEmail = String(email).trim().toLowerCase();
    const normUsername = String(username).trim();

    // check if email or username already exists
    const existingUser = await User.findOne({
      $or: [{ email: normEmail }, { account_name: normUsername }],
    });
    if (existingUser) {
      return res.status(409).json({ error: "Email or username already in use." });
    }

    // hash password and create user
    const hash = await bcrypt.hash(password, 12);
    const user = await User.create({
      nyu_id: NetID,
      email: normEmail,
      account_name: normUsername,
      password: hash,
    });

    // respond (never send password)
    return res.status(201).json({
      id: user._id,
      email: user.email,
      account_name: user.account_name,
    });
  } catch (error) {
    if (error?.code === 11000) {
      return res.status(409).json({ error: "Email or username already in use." });
    }
    console.error("Registration error:", error);
    return res.status(500).json({ error: "Internal server error." });
  }
});

// start server
app.listen(process.env.PORT || 3000, () => {
  console.log(`✅ Server running on port ${process.env.PORT || 3000}`);
});