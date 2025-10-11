import mongoose from "mongoose";

const roommateSchema = new mongoose.Schema({
  title: String,
  images: [String],
  description: String,
  status: String,
  placesToLive: String,
  region: String,
  authorId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  timeUpdate: String,
  timePosted: String,
  favorites: Number,
  onCampus: Boolean,
  year: Number,
});

export default mongoose.model("Roommate", roommateSchema);
