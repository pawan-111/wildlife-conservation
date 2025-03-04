import { Box, Typography } from '@mui/material';
import { Chart as ChartJS, registerables } from 'chart.js';
import React from 'react';
import { Chart } from 'react-chartjs-2';

ChartJS.register(...registerables);

const DetectionHeatmap = () => {
  // TODO: Connect with real detection data
  const data = {
    labels: ['Zone A', 'Zone B', 'Zone C', 'Zone D'],
    datasets: [
      {
        label: 'Detections',
        data: [12, 19, 3, 17],
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)'
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)'
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Detection Heatmap
      </Typography>
      <Chart
        type="bar"
        data={data}
        options={{
          scales: {
            x: {
              type: 'category',
              title: {
                display: true,
                text: 'Zones'
              }
            },
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Detections'
              }
            }
          },
          plugins: {
            legend: {
              display: false
            }
          }
        }}
      />
    </Box>
  );
};

export default DetectionHeatmap;
