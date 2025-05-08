import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Paper,
  CircularProgress,
  Alert
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import FileUpload from './components/FileUpload';
import AnalysisResults from './components/AnalysisResults';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('http://localhost:8000/upload/', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Upload failed');
      }
      
      const data = await response.json();
      setUploadedFile(data);
      
      // Poll for analysis results
      pollAnalysisResults(data.filename);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const pollAnalysisResults = async (filename) => {
    try {
      const response = await fetch(`http://localhost:8000/analysis/${filename}`);
      const data = await response.json();
      
      if (data.status === 'completed') {
        setAnalysisResults(data);
        setLoading(false);
      } else if (data.status === 'pending_analysis') {
        // Poll again after 2 seconds
        setTimeout(() => pollAnalysisResults(filename), 2000);
      }
    } catch (err) {
      setError('Failed to get analysis results');
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            TumorLens
          </Typography>
          <Typography variant="h5" component="h2" gutterBottom align="center" color="text.secondary">
            Brain Tumor Detection System
          </Typography>
          
          <Paper elevation={3} sx={{ p: 3, mt: 4 }}>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            
            <FileUpload onFileUpload={handleFileUpload} disabled={loading} />
            
            {loading && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
                <CircularProgress />
              </Box>
            )}
            
            {analysisResults && (
              <AnalysisResults results={analysisResults} />
            )}
          </Paper>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 