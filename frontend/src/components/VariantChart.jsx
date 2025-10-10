import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Box, Typography, Skeleton, Grid } from '@mui/material';

const COLORS = ['#000000', '#666666', '#999999', '#cccccc', '#333333'];

const VariantChart = ({ data, loading = false }) => {
  if (loading) {
    return (
      <Box sx={{ height: 400 }}>
        <Skeleton variant="rectangular" width="100%" height={400} />
      </Box>
    );
  }

  if (!data) {
    return (
      <Box sx={{ height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Typography color="text.secondary">No data available</Typography>
      </Box>
    );
  }

  // Prepare data for charts
  const chromosomeData = Object.entries(data.by_chromosome || {})
    .map(([chromosome, count]) => ({ chromosome, count }))
    .sort((a, b) => a.chromosome.localeCompare(b.chromosome));

  const impactData = Object.entries(data.by_impact || {})
    .map(([impact, count]) => ({ impact, count }))
    .filter(item => item.impact && item.impact !== 'null');

  return (
    <Box sx={{ height: 400 }}>
      <Grid container spacing={2} sx={{ height: '100%' }}>
        <Grid item xs={12} md={6}>
          <Typography variant="subtitle2" gutterBottom>
            By Chromosome
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={chromosomeData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ chromosome, percent }) => `${chromosome} (${(percent * 100).toFixed(0)}%)`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="count"
              >
                {chromosomeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Typography variant="subtitle2" gutterBottom>
            By Impact
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={impactData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="impact" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </Grid>
      </Grid>
    </Box>
  );
};

export default VariantChart;
