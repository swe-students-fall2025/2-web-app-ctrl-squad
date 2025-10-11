import mongoose from "mongoose";

const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  account_name: { type: String, required: true },
  password: { type: String, required: true },
  bio: String,
  nyu_id: String,
  trades: [{ type: mongoose.Schema.Types.ObjectId, ref: "Trade" }],
  posts: [{ type: mongoose.Schema.Types.ObjectId, ref: "Post" }],
  favorited: [{ postId: mongoose.Schema.Types.ObjectId }],
  usage_type: [String],
});

export default mongoose.model("User", userSchema);
