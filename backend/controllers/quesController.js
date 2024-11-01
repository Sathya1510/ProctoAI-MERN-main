import asyncHandler from "express-async-handler";
import Question from "../models/quesModel.js";

const getQuestionsByExamId = asyncHandler(async (req, res) => {
  const { examId } = req.params;
  console.log("Question Exam id ", examId);

  if (!examId) {
    return res.status(400).json({ error: "examId is missing or invalid" });
  }

  const questions = await Question.find({ examId });
  console.log("Question Exam  ", questions);

  res.status(200).json(questions);
});

const createQuestion = asyncHandler(async (req, res) => {
  const { question, options, examId } = req.body;

  if (!examId) {
    return res.status(400).json({ error: "examId is missing or invalid" });
  }

  const newQuestion = new Question({
    question,
    options,
    examId,
  });

  const createdQuestion = await newQuestion.save();

  if (createdQuestion) {
    res.status(201).json(createdQuestion);
  } else {
    res.status(400);
    throw new Error("Invalid Question Data");
  }
});

const createMultipleQuestions = asyncHandler(async (req, res) => {
  const { questions, examId } = req.body;

  if (!examId) {
    return res.status(400).json({ error: "examId is missing or invalid" });
  }

  if (!Array.isArray(questions) || questions.length === 0) {
    return res.status(400).json({ error: "Questions array is missing or empty" });
  }

  // Add examId to each question before saving
  const questionsWithExamId = questions.map((q) => ({
    ...q,
    examId,
  }));

  try {
    const createdQuestions = await Question.insertMany(questionsWithExamId);
    res.status(201).json(createdQuestions);
  } catch (error) {
    res.status(400).json({ error: "Failed to create questions", details: error.message });
  }
});


export { getQuestionsByExamId, createQuestion, createMultipleQuestions };
