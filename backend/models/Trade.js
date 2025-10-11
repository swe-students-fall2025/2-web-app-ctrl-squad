import mongoose from "mongoose";

const tradeSchema = new mongoose.Schema({
  exchange_type: String,
  item_being_traded: { type: mongoose.Schema.Types.ObjectId, ref: "Post" },
  sender_id: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  receiver_id: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  status: { type: String, default: "ongoing" },
  time_initiated: { type: Date, default: Date.now },
  time_completed: Date,
  categories: [String],
});

export default mongoose.model("Trade", tradeSchema);
