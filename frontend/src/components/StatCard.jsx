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
    primary: '#1976d2',
    secondary: '#dc004e',
    error: '#d32f2f',
    warning: '#ed6c02',
    info: '#0288d1',
    success: '#2e7d32',
  };

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box
            sx={{
              p: 1,
              borderRadius: 1,
              backgroundColor: `${colorMap[color]}20`,
              color: colorMap[color],
              mr: 2,
            }}
          >
            {icon}
          </Box>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {title}
            </Typography>
            {loading ? (
              <Skeleton variant="text" width={60} height={32} />
            ) : (
              <Typography variant="h4" component="div" sx={{ fontWeight: 600 }}>
                {value.toLocaleString()}
              </Typography>
            )}
            {subtitle && (
              <Typography variant="body2" color="text.secondary">
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
