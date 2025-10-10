import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { keyframes } from '@mui/system';

const pulseAnimation = keyframes`
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
`;

const shimmerAnimation = keyframes`
  0% {
    background-position: -200px 0;
  }
  100% {
    background-position: calc(200px + 100%) 0;
  }
`;

const LoadingSpinner = ({ 
  size = 60, 
  message = 'Loading...', 
  fullScreen = false,
  variant = 'circular' // 'circular', 'skeleton', 'dots'
}) => {
  const containerStyles = fullScreen ? {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, rgba(252, 228, 236, 0.9) 0%, rgba(243, 229, 245, 0.9) 100%)',
    backdropFilter: 'blur(10px)',
    zIndex: 9999,
  } : {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    p: 4,
  };

  const renderLoader = () => {
    switch (variant) {
      case 'skeleton':
        return (
          <Box sx={{ width: '100%', maxWidth: 400 }}>
            {[...Array(3)].map((_, index) => (
              <Box
                key={index}
                sx={{
                  height: 20,
                  mb: 2,
                  borderRadius: 1,
                  background: 'linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)',
                  backgroundSize: '200px 100%',
                  animation: `${shimmerAnimation} 1.5s infinite`,
                  opacity: 0.7,
                }}
              />
            ))}
          </Box>
        );
      
      case 'dots':
        return (
          <Box sx={{ display: 'flex', gap: 1 }}>
            {[...Array(3)].map((_, index) => (
              <Box
                key={index}
                sx={{
                  width: 12,
                  height: 12,
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #E91E63, #9C27B0)',
                  animation: `${pulseAnimation} 1.4s infinite`,
                  animationDelay: `${index * 0.2}s`,
                }}
              />
            ))}
          </Box>
        );
      
      default:
        return (
          <CircularProgress
            size={size}
            thickness={4}
            sx={{
              color: '#E91E63',
              '& .MuiCircularProgress-circle': {
                strokeLinecap: 'round',
              },
            }}
          />
        );
    }
  };

  return (
    <Box sx={containerStyles}>
      {renderLoader()}
      {message && (
        <Typography
          variant="body1"
          sx={{
            mt: 2,
            color: '#666666',
            fontWeight: 500,
            background: 'linear-gradient(135deg, #E91E63, #9C27B0)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          {message}
        </Typography>
      )}
    </Box>
  );
};

export default LoadingSpinner;
