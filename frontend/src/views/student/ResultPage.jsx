import React, {useState, useEffect} from 'react';
import { Typography } from '@mui/material';
import PageContainer from 'src/components/container/PageContainer';
import DashboardCard from '../../components/shared/DashboardCard';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { NightShelter } from '@mui/icons-material';

const ResultPage = () => {
  const [result, setResult] = useState([])
  const userEmail = 'suryaroxx@gmail.com';
  const fetchUserResult = async () => {
    try {
      const userInfo = localStorage.getItem('userInfo') ? JSON.parse(localStorage.getItem('userInfo')) : null;
      let email = userInfo.role === "student" ? userInfo?.email: "false";
      const response = await fetch(`http://localhost:5000/api/users/get-result/${email}`);
      if (!response.ok) {
        throw new Error('Failed to fetch user result');
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error fetching user result:', error);
    }
  };
  console.log(result)
  // Call the fetchUserResult function when the component mounts
  useEffect(() => {
    fetchUserResult();
  }, []);



  return (
    <PageContainer title="Result Page" description="this is Result page">
      <DashboardCard title="Result Page">
        <Typography>This is a Result page</Typography>
        <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>S.no</TableCell>
                        <TableCell>Email</TableCell>
                        <TableCell>Username</TableCell>
                        <TableCell>Correct Answer</TableCell>
                        <TableCell>Total Count</TableCell>
                        <TableCell>Exam Id</TableCell>
                        <TableCell>Submitted Date</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {result.map((row, index) => (
                        <TableRow key={row._id}>
                            <TableCell>{index + 1}</TableCell>
                            <TableCell>{row.email}</TableCell>
                            <TableCell>{row.username}</TableCell>
                            <TableCell>{row.correctAnswer}</TableCell>
                            <TableCell>{row.totalCount}</TableCell>
                            <TableCell>{row.examId.substring(0, 8)}</TableCell>
                            <TableCell>{new Date(row.updatedAt).toLocaleString()}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
      </DashboardCard>
    </PageContainer>
  );
};

export default ResultPage;
