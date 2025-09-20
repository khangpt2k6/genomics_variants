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
        background: 'rgba(255, 255, 255, 0.08)',
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.12)',
        color: '#ffffff',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)'
      }}
    >
      <Toolbar>
        <Typography 
          variant="h6" 
          component="div" 
          sx={{ 
            flexGrow: 1, 
            fontWeight: 600,
            color: '#ffffff',
            textShadow: '0 2px 4px rgba(0, 0, 0, 0.3)'
          }}
        >
          Moffitt Variant Dashboard
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <IconButton 
            sx={{ 
              color: '#ffffff',
              '&:hover': {
                background: 'rgba(255, 255, 255, 0.1)',
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
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: '2px solid rgba(255, 255, 255, 0.2)',
              boxShadow: '0 4px 16px rgba(0, 0, 0, 0.3)'
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
