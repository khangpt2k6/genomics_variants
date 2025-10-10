import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box, useMediaQuery, useTheme } from '@mui/material';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import MobileNav from './components/MobileNav';
import ErrorBoundary from './components/ErrorBoundary';
import Dashboard from './pages/Dashboard';
import Variants from './pages/Variants';
import Annotations from './pages/Annotations';
import GalaxyIntegration from './pages/GalaxyIntegration';
import VariantDetail from './pages/VariantDetail';

function App() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  return (
    <Box sx={{ 
      display: 'flex', 
      minHeight: '100vh',
      background: '#ffffff',
    }}>
      {/* Mobile Navigation */}
      <MobileNav />
      
      {/* Desktop Sidebar */}
      {!isMobile && <Sidebar />}
      
      <Box sx={{ 
        flexGrow: 1, 
        display: 'flex', 
        flexDirection: 'column',
        pt: { xs: 7, md: 0 } // Add top padding for mobile nav
      }}>
        {/* Desktop Navbar */}
        {!isMobile && <Navbar />}
        
        <Box component="main" sx={{ 
          flexGrow: 1, 
          p: { xs: 2, md: 3 },
          background: 'transparent'
        }}>
          <ErrorBoundary>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/variants" element={<Variants />} />
              <Route path="/variants/:id" element={<VariantDetail />} />
              <Route path="/annotations" element={<Annotations />} />
              <Route path="/galaxy" element={<GalaxyIntegration />} />
            </Routes>
          </ErrorBoundary>
        </Box>
      </Box>
    </Box>
  );
}

export default App;