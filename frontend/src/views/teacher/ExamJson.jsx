import React, { useState, useEffect } from 'react';
import { TextField, Button, Typography, Box, Select, MenuItem } from '@mui/material';
import { useCreateMultipleQuestionsMutation, useGetExamsQuery } from 'src/slices/examApiSlice';
import swal from 'sweetalert';
import { toast } from 'react-toastify';

const ExamJsonForm = () => {
  const [jsonData, setJsonData] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [selectedExamId, setSelectedExamId] = useState('');
  const { data: examsData } = useGetExamsQuery();
  const [createMultipleQuestions] = useCreateMultipleQuestionsMutation();

  useEffect(() => {
    if (examsData && examsData.length > 0) {
      setSelectedExamId(examsData[0].examId);
    }
  }, [examsData]);

  const handleAddQuestion = async () => {
    try {
      const parsedQuestions = JSON.parse(jsonData);

      if (!Array.isArray(parsedQuestions)) {
        setError("JSON data must be an array of questions.");
        return;
      }

      const newQuestionObj = {
        questions: parsedQuestions,
        examId: selectedExamId,
      };
      console.log(newQuestionObj)
      const res = await createMultipleQuestions(newQuestionObj).unwrap();
      if (res) {
        toast.success('Questions added successfully!');
        setSuccessMessage('Questions added successfully!');
        setJsonData(''); // Clear input after successful submission
      }
    } catch (err) {
      setError("Invalid JSON format. Please check your input.");
      swal('', 'Failed to create questions. Please try again.', 'error');
    }
  };

  return (
    <Box>
      <Box sx={{ p: 3, maxWidth: 600, margin: '0 auto' }}>
        <Typography variant="h5" gutterBottom>
          Select Exam
        </Typography>

        <Select
          label="Select Exam"
          value={selectedExamId}
          onChange={(e) => setSelectedExamId(e.target.value)}
          fullWidth
          sx={{ mb: 2 }}
        >
          {examsData &&
            examsData.map((exam) => (
              <MenuItem key={exam.examId} value={exam.examId}>
                {exam.examName}
              </MenuItem>
            ))}
        </Select>

        <Typography variant="h5" gutterBottom>
          Submit Exam JSON Data
        </Typography>
        <TextField
          label="Enter JSON Data"
          multiline
          rows={10}
          variant="outlined"
          fullWidth
          value={jsonData}
          onChange={(e) => setJsonData(e.target.value)}
          placeholder={`[
    {
      "question": "What is AI's full form?",
      "options": [
        { "optionText": "Artificial Intelligence", "isCorrect": true },
        { "optionText": "Automated Intelligence", "isCorrect": false },
        { "optionText": "Applied Intelligence", "isCorrect": false },
        { "optionText": "Actual Intelligence", "isCorrect": false }
      ]
    }
  ]`}
        />
        {error && <Typography color="error">{error}</Typography>}
        {successMessage && <Typography color="success.main">{successMessage}</Typography>}
        <Button variant="contained" color="primary" onClick={handleAddQuestion} sx={{ mt: 2 }}>
          Submit
        </Button>
      </Box>
    </Box>
  );
};

export default ExamJsonForm;
