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
        background: 'rgba(255, 255, 255, 0.06)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        borderRadius: 3,
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
        transition: 'all 0.3s ease',
        '&:hover': {
          background: 'rgba(255, 255, 255, 0.08)',
          borderColor: 'rgba(255, 255, 255, 0.15)',
          transform: 'translateY(-4px)',
          boxShadow: '0 12px 48px rgba(0, 0, 0, 0.4)',
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
                color: 'rgba(255, 255, 255, 0.7)',
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
                  color: '#ffffff',
                  textShadow: '0 2px 4px rgba(0, 0, 0, 0.3)',
                  background: `linear-gradient(135deg, #ffffff, ${colorMap[color]})`,
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                {value.toLocaleString()}
              </Typography>
            )}
            {subtitle && (
              <Typography 
                variant="body2" 
                sx={{ 
                  color: 'rgba(255, 255, 255, 0.6)',
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
