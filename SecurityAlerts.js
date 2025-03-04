import { Alert, AlertTitle, Paper, Typography } from '@mui/material';
import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

// Configure WebSocket client with matching keep-alive settings
const socket = io('http://localhost:5001', {
  transports: ['websocket'],
  pingTimeout: 60000,
  pingInterval: 25000,
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  autoConnect: true,
  withCredentials: true
});

const SecurityAlerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Initialize connection
    socket.connect();

    // Handle connection events
    socket.on('connect', () => {
      console.log('Connected to WebSocket server');
      setIsConnected(true);
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
      setIsConnected(false);
    });

    socket.on('connect_error', (err) => {
      console.error('WebSocket connection error:', err);
    });

    // Listen for detection events from the server
    socket.on('detection', (detection) => {
      console.log('Received detection:', detection);
      const newAlert = {
        type: detection.class === 'gun' ? 'error' : 'info',
        message: `${detection.class} detected in ${detection.zone}`,
        confidence: detection.confidence,
        timestamp: new Date().toLocaleTimeString()
      };
      console.log('Creating new alert:', newAlert);
      setAlerts((prevAlerts) => {
        const updatedAlerts = [newAlert, ...prevAlerts].slice(0, 5);
        console.log('Updated alerts:', updatedAlerts);
        return updatedAlerts;
      });
    });

    // Cleanup on unmount
    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('connect_error');
      socket.off('detection');
      socket.disconnect();
    };
  }, []);

  return (
    <Paper elevation={3} sx={{ p: 2, maxHeight: 300, overflow: 'auto' }}>
      {!isConnected && (
        <Alert severity="warning" sx={{ mb: 2 }}>
          Not connected to WebSocket server. Alerts may not be received.
        </Alert>
      )}
      {alerts.length === 0 && (
        <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
          No security alerts detected
        </Typography>
      )}
      <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
        Security Alerts
      </Typography>
      {alerts.map((alert, index) => (
        <Alert
          key={index}
          severity={alert.type}
          sx={{
            mb: 1,
            '& .MuiAlert-message': {
              fontSize: '0.875rem'
            }
          }}
        >
          <AlertTitle sx={{ fontSize: '0.9rem' }}>
            {alert.type === 'error' ? '🚨 Critical Alert' : 'ℹ️ Security Alert'}
          </AlertTitle>
          {alert.message} (Confidence: {(alert.confidence * 100).toFixed(1)}%)<br/>
          <Typography variant="caption" sx={{ mt: 0.5, display: 'block' }}>
            Detected at: {alert.timestamp}
          </Typography>
        </Alert>
      ))}
    </Paper>
  );
};

export default SecurityAlerts;
