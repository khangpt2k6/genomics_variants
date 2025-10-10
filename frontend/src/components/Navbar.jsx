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
        background: '#ffffff',
        borderBottom: '1px solid #e0e0e0',
        color: 'text.primary',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
      }}
    >
      <Toolbar>
        <Typography 
          variant="h6" 
          component="div" 
          sx={{ 
            flexGrow: 1, 
            fontWeight: 600,
            color: '#000000',
          }}
        >
          Variant Dashboard
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <IconButton 
            sx={{ 
              color: 'text.primary',
              '&:hover': {
                background: 'rgba(0, 0, 0, 0.04)',
              },
              transition: 'all 0.2s ease'
            }}
          >
            <Badge 
              badgeContent={4} 
              sx={{
                '& .MuiBadge-badge': {
                  backgroundColor: '#000000',
                  color: '#ffffff',
                }
              }}
            >
              <NotificationsIcon />
            </Badge>
          </IconButton>
          
          <IconButton 
            sx={{ 
              '&:hover': {
                background: 'rgba(0, 0, 0, 0.04)'
              },
              transition: 'all 0.2s ease'
            }}
          >
            <Avatar sx={{ 
              width: 32, 
              height: 32, 
              background: '#000000',
              border: '2px solid #e0e0e0',
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
