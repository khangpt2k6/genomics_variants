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
    primary: '#667eea',
    secondary: '#f093fb',
    error: '#ff6b6b',
    warning: '#feca57',
    info: '#48dbfb',
    success: '#1dd1a1',
  };

  return (
    <Card 
      sx={{ 
        height: '100%',
        background: (theme) => theme.palette.background.paper,
        border: '1px solid rgba(0, 0, 0, 0.08)',
        borderRadius: 3,
        boxShadow: '0 4px 18px rgba(0, 0, 0, 0.08)',
        transition: 'box-shadow 0.2s ease, transform 0.2s ease',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: '0 10px 28px rgba(0, 0, 0, 0.12)',
        }
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box
            sx={{
              p: 2,
              borderRadius: 2,
              background: `linear-gradient(135deg, ${colorMap[color]}20, ${colorMap[color]}10)`,
              border: `1px solid ${colorMap[color]}30`,
              color: colorMap[color],
              mr: 2,
              boxShadow: `0 4px 16px ${colorMap[color]}20`,
              transition: 'all 0.3s ease',
              '&:hover': {
                transform: 'scale(1.05) rotate(5deg)',
                boxShadow: `0 8px 24px ${colorMap[color]}30`,
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
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
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
