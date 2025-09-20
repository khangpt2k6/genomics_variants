import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
  Divider,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Science as ScienceIcon,
  Assignment as AssignmentIcon,
  CloudUpload as CloudUploadIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Variants', icon: <ScienceIcon />, path: '/variants' },
  { text: 'Annotations', icon: <AssignmentIcon />, path: '/annotations' },
  { text: 'Galaxy Integration', icon: <CloudUploadIcon />, path: '/galaxy' },
];

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          background: 'rgba(255, 255, 255, 0.06)',
          backdropFilter: 'blur(20px)',
          borderRight: '1px solid rgba(255, 255, 255, 0.12)',
          boxShadow: '8px 0 32px rgba(0, 0, 0, 0.3)',
        },
      }}
    >
      <Box sx={{ p: 2 }}>
        <Typography 
          variant="h6" 
          sx={{ 
            fontWeight: 600, 
            color: '#ffffff',
            textShadow: '0 2px 4px rgba(0, 0, 0, 0.3)',
            mb: 0.5
          }}
        >
          Moffitt Cancer Center
        </Typography>
        <Typography 
          variant="body2" 
          sx={{ 
            color: 'rgba(255, 255, 255, 0.7)',
            fontSize: '0.75rem',
            fontWeight: 400
          }}
        >
          Variant Interpretation Platform
        </Typography>
      </Box>
      
      <Divider sx={{ borderColor: 'rgba(255, 255, 255, 0.12)' }} />
      
      <List sx={{ px: 1, py: 2 }}>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => navigate(item.path)}
              sx={{
                borderRadius: 2,
                mx: 0.5,
                transition: 'all 0.3s ease',
                '&.Mui-selected': {
                  background: 'rgba(255, 255, 255, 0.15)',
                  color: '#ffffff',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  boxShadow: '0 4px 16px rgba(0, 0, 0, 0.2)',
                  '&:hover': {
                    background: 'rgba(255, 255, 255, 0.2)',
                    transform: 'translateX(4px)'
                  },
                },
                '&:hover': {
                  background: 'rgba(255, 255, 255, 0.08)',
                  transform: 'translateX(2px)',
                  color: '#ffffff'
                },
                color: location.pathname === item.path ? '#ffffff' : 'rgba(255, 255, 255, 0.8)'
              }}
            >
              <ListItemIcon
                sx={{
                  color: location.pathname === item.path ? '#ffffff' : 'rgba(255, 255, 255, 0.7)',
                  minWidth: 40,
                  transition: 'all 0.3s ease'
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText 
                primary={item.text}
                sx={{
                  '& .MuiListItemText-primary': {
                    fontWeight: location.pathname === item.path ? 600 : 400,
                    fontSize: '0.9rem'
                  }
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;

