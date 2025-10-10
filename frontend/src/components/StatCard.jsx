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
    primary: '#E91E63', // Pink
    secondary: '#9C27B0', // Purple
    error: '#F44336',
    warning: '#FF9800',
    info: '#2196F3',
    success: '#4CAF50',
  };

  return (
    <Card 
      sx={{ 
        height: '100%',
        background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 187, 208, 0.1) 50%, rgba(156, 39, 176, 0.1) 100%)',
        border: '1px solid rgba(233, 30, 99, 0.1)',
        borderRadius: 3,
        boxShadow: '0 8px 32px rgba(233, 30, 99, 0.15)',
        backdropFilter: 'blur(20px)',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 12px 48px rgba(233, 30, 99, 0.25)',
          borderColor: 'rgba(233, 30, 99, 0.2)',
        }
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box
            sx={{
              p: 2,
              borderRadius: 2,
              background: `linear-gradient(135deg, ${colorMap[color]}30, ${colorMap[color]}15)`,
              border: `1px solid ${colorMap[color]}40`,
              color: colorMap[color],
              mr: 2,
              boxShadow: `0 4px 16px ${colorMap[color]}25`,
              transition: 'all 0.3s ease',
              '&:hover': {
                transform: 'scale(1.1) rotate(8deg)',
                boxShadow: `0 8px 24px ${colorMap[color]}35`,
                background: `linear-gradient(135deg, ${colorMap[color]}40, ${colorMap[color]}20)`,
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
