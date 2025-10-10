import React from 'react';
import {
  Card,
  CardContent,
  Box,
  Typography,
  Skeleton,
} from '@mui/material';

const StatCard = ({
  title,
  value,
  icon,
  color,
  loading = false,
  subtitle,
}) => {
  const colorMap = {
    primary: '#000000', // Black
    secondary: '#666666', // Dark gray
    error: '#000000',
    warning: '#666666',
    info: '#000000',
    success: '#000000',
  };

  return (
    <Card 
      sx={{ 
        height: '100%',
        background: '#ffffff',
        border: '1px solid #e0e0e0',
        borderRadius: 2,
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
        transition: 'all 0.2s ease',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: '0 4px 16px rgba(0, 0, 0, 0.15)',
        }
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box
            sx={{
              p: 2,
              borderRadius: 2,
              background: '#f5f5f5',
              border: `1px solid ${colorMap[color]}`,
              color: colorMap[color],
              mr: 2,
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
              transition: 'all 0.2s ease',
              '&:hover': {
                transform: 'scale(1.05)',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.15)',
                background: '#e0e0e0',
              }
            }}
          >
            {icon}
          </Box>
          <Box sx={{ flexGrow: 1 }}>
            <Typography 
              variant="body2" 
              sx={{ 
                color: 'text.secondary',
                fontWeight: 500,
                mb: 1,
                fontSize: '0.85rem',
                textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }} 
              gutterBottom
            >
              {title}
            </Typography>
            {loading ? (
              <Skeleton 
                variant="text" 
                width={60} 
                height={32} 
                sx={{ 
                  backgroundColor: '#e0e0e0',
                  borderRadius: 1
                }} 
              />
            ) : (
              <Typography 
                variant="h4" 
                component="div" 
                sx={{ 
                  fontWeight: 700,
                  color: 'text.primary'
                }}
              >
                {value.toLocaleString()}
              </Typography>
            )}
            {subtitle && (
              <Typography 
                variant="body2" 
                sx={{ 
                  color: 'text.secondary',
                  fontSize: '0.75rem',
                  mt: 0.5
                }}
              >
                {subtitle}
              </Typography>
            )}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default StatCard;
