import asyncHandler from "express-async-handler";
import User from "./../models/userModel.js";
import Result from "./../models/resultModel.js"
import generateToken from "../utils/generateToken.js";

const authUser = asyncHandler(async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });

  if (user && (await user.matchPassword(password))) {
    generateToken(res, user._id);

    res.status(201).json({
      _id: user._id,
      name: user.name,
      email: user.email,
      role: user.role,
      password_encrypted: user.password,
      message: "User Successfully login with role: " + user.role,
    });
  } else {
    res.status(401);
    throw new Error("Invalid User email or password ");
  }
});

const registerUser = asyncHandler(async (req, res) => {
  const { name, email, password, role } = req.body;

  const userExist = await User.findOne({ email });

  if (userExist) {
    res.status(400);
    throw new Error("User Already Exists");
  }

  const user = await User.create({
    name,
    email,
    password,
    role,
  });
  console.log(user)
  if (user) {
    generateToken(res, user._id);

    res.status(201).json({
      _id: user._id,
      name: user.name,
      email: user.email,
      role: user.role,
      password_encrypted: user.password,
      message: "User Successfully created with role: " + user.role,
    });
  } else {
    res.status(400);
    throw new Error("Invalid User Data");
  }
});

const logoutUser = asyncHandler(async (req, res) => {
  res.cookie("jwt", "", {
    httpOnly: true,
    expires: new Date(0),
  });
  res.status(200).json({ message: " User logout User" });
});

const getUserProfile = asyncHandler(async (req, res) => {
  const user = {
    _id: req.user._id,
    name: req.user.name,
    email: req.user.email,
    role: req.user.role,
  };
  res.status(200).json(user);
});

const updateUserProfile = asyncHandler(async (req, res) => {
  const user = await User.findById(req.user._id);

  if (user) {
    user.name = req.body.name || user.name;
    user.email = req.body.email || user.email;
    user.role = req.body.role || user.role;

    if (req.body.password) {
      user.password = req.body.password;
    }

    const updatedUser = await user.save();
    res.status(200).json({
      _id: updatedUser._id,
      name: updatedUser.name,
      email: updatedUser.email,
      role: updatedUser.role,
    });
  } else {
    res.status(404);
    throw new Error("User Not Found");
  }
});

const createUserTestResult = asyncHandler(async (req, res) => {
  console.log(req.body, "hihi")
  const { totalCount, correctAnswer, examId, email, username } = req.body;

  if (!email || !examId || !username) {
    res.status(400);
    throw new Error("Email, Exam ID, and Username are required fields");
  }

  // Create a new result document
  const newResult = new Result({
    totalCount,
    correctAnswer,
    examId,
    email,
    username,
  });

  const savedResult = await newResult.save();

  res.status(201).json({
    _id: savedResult._id,
    totalCount: savedResult.totalCount,
    correctAnswer: savedResult.correctAnswer,
    examId: savedResult.examId,
    email: savedResult.email,
    username: savedResult.username,
    createdAt: savedResult.createdAt,
    updatedAt: savedResult.updatedAt,
  });
});
const getUserTestResultsByEmail = asyncHandler(async (req, res) => {
  const { id } = req.params; // Extract the email (id) from request parameters

  let results;
  console.log(id, "id")
  if (id !== "false") {
    console.log("if")
    // If id (email) is provided, find the result for that particular email
    results = await Result.find({ email: id });

    if (!results) {
      res.status(404);
      throw new Error("No result found for the provided email");
    }
  } else {
    console.log("else")
    // If no id (email) is provided, return all results
    results = await Result.find();

    if (!results || results.length === 0) {
      res.status(404);
      throw new Error("No results found");
    }
  }

  res.status(200).json(results);
});

export {
  authUser,
  registerUser,
  logoutUser,
  getUserProfile,
  updateUserProfile,
  createUserTestResult,
  getUserTestResultsByEmail
};
