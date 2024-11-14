import express from "express";
import {
  authUser,
  getUserProfile,
  logoutUser,
  registerUser,
  updateUserProfile,
  createUserTestResult,
  getUserTestResultsByEmail
} from "../controllers/userController.js";
import { protect } from "../middleware/authMiddleware.js";
import { createExam, getExams } from "../controllers/examController.js";
const userRoutes = express.Router();
userRoutes.post("/", registerUser);
userRoutes.post("/auth", authUser);
userRoutes.post("/logout", logoutUser);
userRoutes.post("/register", registerUser);
userRoutes.post("/submit-result", createUserTestResult);
userRoutes.get("/get-result/:id", getUserTestResultsByEmail);


// protecting profile route using auth middleware protect
userRoutes
  .route("/profile")
  .get(protect, getUserProfile)
  .put(protect, updateUserProfile)

export default userRoutes;
