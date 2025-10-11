import mongoose from "mongoose";

const chatSchema = new mongoose.Schema({
  friendId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  friendProfilePic: String,
  messages: [
    {
      from: String,
      text: String,
      time: String,
    },
  ],
  timeUpdated: String,
});

export default mongoose.model("Chat", chatSchema);
