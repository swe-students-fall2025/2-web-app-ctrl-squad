import express from "express";
import mongoose from "mongoose";
import dotenv from "dotenv";
import cors from "cors"; 
import bcrypt from "bcrypt";
import User from "./models/User.js";
import postRoutes from "./routes/postRoutes.js";
import roommateRoutes from "./routes/roommateRoutes.js";
import userRoutes from "./routes/userRoutes.js";
import { errorHandler } from "./middleware/errorHandler.js";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log("Connected to MongoDB"))
  .catch(err => console.error("MongoDB connection error:", err));

// Health check route
app.get("/", (req, res) => res.send("Backend running!"));

// Routes
app.use("/api/posts", postRoutes);
app.use("/api/roommates", roommateRoutes);
app.use("/api/users", userRoutes);

// Registration route
app.post("/register", async (req, res) => {
  try {
    const { NetID, email, username, password } = req.body;
    if (!NetID || !email || !username || !password) {
      return res.status(400).json({ error: "All fields are required." });
    }

    const normEmail = String(email).trim().toLowerCase();
    const normUsername = String(username).trim();

    const existingUser = await User.findOne({
      $or: [{ email: normEmail }, { account_name: normUsername }],
    });
    if (existingUser) {
      return res.status(409).json({ error: "Email or username already in use." });
    }

    const hash = await bcrypt.hash(password, 12);
    const user = await User.create({
      nyu_id: NetID,
      email: normEmail,
      account_name: normUsername,
      password: hash,
    });

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

// Error handling middleware
app.use(errorHandler);

//  Only ONE listen call
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
