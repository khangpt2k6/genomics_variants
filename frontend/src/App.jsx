import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import ErrorBoundary from './components/ErrorBoundary';
import Dashboard from './pages/Dashboard';
import Variants from './pages/Variants';
import Annotations from './pages/Annotations';
import GalaxyIntegration from './pages/GalaxyIntegration';
import VariantDetail from './pages/VariantDetail';
import VariantNetwork from './pages/VariantNetwork';
import InteractiveVisualization from './components/InteractiveVisualization';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Navbar */}
        <Navbar onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
        
        {/* Page Content */}
        <main className="flex-1 overflow-auto">
          <div className="p-4 md:p-6 lg:p-8">
            <ErrorBoundary>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/variants" element={<Variants />} />
                <Route path="/variants/:id" element={<VariantDetail />} />
                <Route path="/network" element={<VariantNetwork />} />
                <Route path="/visualize" element={<InteractiveVisualization />} />
                <Route path="/annotations" element={<Annotations />} />
                <Route path="/galaxy" element={<GalaxyIntegration />} />
              </Routes>
            </ErrorBoundary>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
