import mongoose from "mongoose";

const postSchema = new mongoose.Schema({
  title: String,
  images: [String],
  description: String,
  exchange_type: String,
  status: String,
  condition: String,
  location: String,
  author_id: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  time_updated: Date,
  time_posted: { type: Date, default: Date.now },
  favorites: Number,
  categories: [String],
});

export default mongoose.model("Post", postSchema);
