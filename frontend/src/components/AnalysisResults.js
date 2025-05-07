import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Chip,
  Divider,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';

const AnalysisResults = ({ results }) => {
  const isTumorDetected = results.prediction > 0.5;
  const confidence = (results.prediction * 100).toFixed(2);

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h5" gutterBottom>
        Analysis Results
      </Typography>
      <Divider sx={{ mb: 3 }} />

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Diagnosis
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              {isTumorDetected ? (
                <WarningIcon color="error" sx={{ mr: 1 }} />
              ) : (
                <CheckCircleIcon color="success" sx={{ mr: 1 }} />
              )}
              <Typography variant="body1">
                {isTumorDetected
                  ? 'Tumor Detected'
                  : 'No Tumor Detected'}
              </Typography>
            </Box>
            <Chip
              label={`Confidence: ${confidence}%`}
              color={isTumorDetected ? 'error' : 'success'}
              variant="outlined"
            />
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Additional Information
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              This analysis is based on the BraTS 2020 dataset and uses a deep learning model
              trained on multiple MRI modalities.
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Note: This is an automated analysis and should be reviewed by a medical professional.
            </Typography>
          </Paper>
        </Grid>

        {results.visualization && (
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Visualization
              </Typography>
              <Box
                component="img"
                src={results.visualization}
                alt="Tumor visualization"
                sx={{
                  width: '100%',
                  maxHeight: 400,
                  objectFit: 'contain',
                }}
              />
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default AnalysisResults; 