import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Badge,
  Avatar,
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  AccountCircle as AccountCircleIcon,
} from '@mui/icons-material';

const Navbar = () => {
  return (
    <AppBar 
      position="static" 
      elevation={0} 
      sx={{ 
        background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(252, 228, 236, 0.8) 100%)',
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(233, 30, 99, 0.1)',
        color: 'text.primary',
        boxShadow: '0 4px 16px rgba(233, 30, 99, 0.1)'
      }}
    >
      <Toolbar>
        <Typography 
          variant="h6" 
          component="div" 
          sx={{ 
            flexGrow: 1, 
            fontWeight: 600,
            background: 'linear-gradient(135deg, #E91E63, #9C27B0)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          Moffitt Variant Dashboard
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <IconButton 
            sx={{ 
              color: 'text.primary',
              '&:hover': {
                background: 'rgba(0, 0, 0, 0.04)',
                transform: 'scale(1.05)'
              },
              transition: 'all 0.3s ease'
            }}
          >
            <Badge 
              badgeContent={4} 
              sx={{
                '& .MuiBadge-badge': {
                  backgroundColor: '#ff4757',
                  color: '#ffffff',
                  boxShadow: '0 0 8px rgba(255, 71, 87, 0.5)'
                }
              }}
            >
              <NotificationsIcon />
            </Badge>
          </IconButton>
          
          <IconButton 
            sx={{ 
              '&:hover': {
                transform: 'scale(1.05)'
              },
              transition: 'all 0.3s ease'
            }}
          >
            <Avatar sx={{ 
              width: 32, 
              height: 32, 
              background: 'linear-gradient(135deg, #E91E63 0%, #9C27B0 100%)',
              border: '2px solid rgba(233, 30, 99, 0.2)',
              boxShadow: '0 4px 16px rgba(233, 30, 99, 0.2)'
            }}>
              <AccountCircleIcon />
            </Avatar>
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
