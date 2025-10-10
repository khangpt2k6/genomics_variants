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
          background: '#ffffff',
          borderRight: '1px solid #e0e0e0',
          boxShadow: '2px 0 8px rgba(0, 0, 0, 0.1)',
        },
      }}
    >
      <Box sx={{ p: 2 }}>
        <Typography 
          variant="h6" 
          sx={{ 
            fontWeight: 600, 
            color: '#000000',
            mb: 0.5
          }}
        >
          Cancer Center
        </Typography>
        <Typography 
          variant="body2" 
          sx={{ 
            color: 'text.secondary',
            fontSize: '0.75rem',
            fontWeight: 400
          }}
        >
          Variant Interpretation Platform
        </Typography>
      </Box>
      
      <Divider sx={{ borderColor: '#e0e0e0' }} />
      
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
                  background: '#f5f5f5',
                  color: 'text.primary',
                  border: '1px solid #e0e0e0',
                  boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                  '&:hover': {
                    background: '#e0e0e0',
                    transform: 'translateX(2px)'
                  },
                },
                '&:hover': {
                  background: '#f9f9f9',
                  transform: 'translateX(1px)',
                  color: 'text.primary'
                },
                color: location.pathname === item.path ? 'text.primary' : 'text.secondary'
              }}
            >
              <ListItemIcon
                sx={{
                  color: location.pathname === item.path ? 'text.primary' : 'text.secondary',
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

