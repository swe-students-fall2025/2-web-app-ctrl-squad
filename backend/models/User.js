import mongoose from "mongoose";

const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  account_name: { type: String, required: true },
  password: { type: String, required: true },
  bio: String,
  nyu_id: { type: String, required: true, trim: true },
  
  profile_image: { type: String, default: "" },

  trades: [{ type: mongoose.Schema.Types.ObjectId, ref: "Trade" }],
  posts: [{ type: mongoose.Schema.Types.ObjectId, ref: "Post" }],
  favorited: [{ type: mongoose.Schema.Types.ObjectId, ref: "Post" }],
  usage_type: [String],
}, { timestamps: true });

export default mongoose.model("User", userSchema);
