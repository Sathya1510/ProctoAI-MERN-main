import mongoose from "mongoose";

// Define a schema for the cheating log
const resultSchema = new mongoose.Schema(
  {
    totalCount: { type: Number, default: 0 },
    correctAnswer: { type: Number, default: 0 },
    examId: { type: String, required: true },
    email: { type: String, required: true },
    username: { type: String, required: true },
  },
  {
    timestamps: true,
  }
);

// Create a model using the schema
const Result = mongoose.model("Result", resultSchema);

export default Result;
