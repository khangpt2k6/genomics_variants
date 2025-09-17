import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Variants from './pages/Variants';
import Annotations from './pages/Annotations';
import GalaxyIntegration from './pages/GalaxyIntegration';
import VariantDetail from './pages/VariantDetail';

function App() {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <Navbar />
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/variants" element={<Variants />} />
            <Route path="/variants/:id" element={<VariantDetail />} />
            <Route path="/annotations" element={<Annotations />} />
            <Route path="/galaxy" element={<GalaxyIntegration />} />
          </Routes>
        </Box>
      </Box>
    </Box>
  );
}

export default App;