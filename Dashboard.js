import { Box, Grid, Typography } from '@mui/material';
import React from 'react';
import DetectionHeatmap from './DetectionHeatmap';
import PopulationEstimation from './PopulationEstimation';
import SecurityAlerts from './SecurityAlerts';
import SpeciesDistribution from './SpeciesDistribution';

const Dashboard = () => {
  return (
    <Box sx={{ p: 2, bgcolor: '#121212', borderRadius: '8px' }}>
      <Typography variant="h5" gutterBottom color="primary">
        Wildlife Monitoring Dashboard
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <SecurityAlerts />
        </Grid>
        <Grid item xs={12} md={6}>
          <DetectionHeatmap />
        </Grid>
        <Grid item xs={12} md={6}>
          <SpeciesDistribution />
        </Grid>
        <Grid item xs={12} md={6}>
          <PopulationEstimation />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
