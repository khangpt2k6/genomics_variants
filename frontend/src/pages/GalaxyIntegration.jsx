import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  Refresh as RefreshIcon,
  PlayArrow as PlayIcon,
  Stop as StopIcon,
} from '@mui/icons-material';

const GalaxyIntegration = () => {
  // Mock data for demonstration
  const galaxyInstances = [
    {
      id: 1,
      name: 'Cancer Center Galaxy',
      url: 'https://galaxy.moffitt.org',
      status: 'active',
      lastSync: '2024-01-15T10:30:00Z',
      datasets: 1250,
      workflows: 45,
    },
    {
      id: 2,
      name: 'Public Galaxy',
      url: 'https://usegalaxy.org',
      status: 'inactive',
      lastSync: '2024-01-10T15:45:00Z',
      datasets: 890,
      workflows: 23,
    },
  ];

  const recentDatasets = [
    {
      id: 1,
      name: 'Patient_001_variants.vcf',
      type: 'VCF',
      size: '2.5 MB',
      status: 'processed',
      created: '2024-01-15T10:30:00Z',
    },
    {
      id: 2,
      name: 'Cohort_analysis_results.txt',
      type: 'TXT',
      size: '1.2 MB',
      status: 'processing',
      created: '2024-01-15T09:15:00Z',
    },
    {
      id: 3,
      name: 'Annotation_output.csv',
      type: 'CSV',
      size: '850 KB',
      status: 'completed',
      created: '2024-01-14T16:20:00Z',
    },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
      case 'completed':
      case 'processed':
        return 'success';
      case 'processing':
        return 'info';
      case 'inactive':
      case 'failed':
        return 'error';
      case 'pending':
        return 'warning';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Galaxy Integration
        </Typography>
        <Button
          variant="contained"
          startIcon={<CloudUploadIcon />}
          onClick={() => {
            // Implement sync with Galaxy
            console.log('Sync with Galaxy');
          }}
        >
          Sync with Galaxy
        </Button>
      </Box>

      {/* Galaxy Instances */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Galaxy Instances
          </Typography>
          <Grid container spacing={2}>
            {galaxyInstances.map((instance) => (
              <Grid item xs={12} md={6} key={instance.id}>
                <Card variant="outlined">
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                      <Typography variant="h6">{instance.name}</Typography>
                      <Chip
                        label={instance.status}
                        color={getStatusColor(instance.status)}
                        size="small"
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      URL: {instance.url}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      Last Sync: {new Date(instance.lastSync).toLocaleString()}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                      <Typography variant="body2">
                        <strong>{instance.datasets}</strong> datasets
                      </Typography>
                      <Typography variant="body2">
                        <strong>{instance.workflows}</strong> workflows
                      </Typography>
                    </Box>
                    <Box sx={{ mt: 2 }}>
                      <Button
                        size="small"
                        startIcon={<RefreshIcon />}
                        onClick={() => console.log(`Sync ${instance.name}`)}
                      >
                        Sync Now
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Recent Datasets */}
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              Recent Datasets
            </Typography>
            <Button
              startIcon={<RefreshIcon />}
              onClick={() => console.log('Refresh datasets')}
            >
              Refresh
            </Button>
          </Box>

          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Size</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {recentDatasets.map((dataset) => (
                  <TableRow key={dataset.id}>
                    <TableCell>
                      <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                        {dataset.name}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip label={dataset.type} size="small" variant="outlined" />
                    </TableCell>
                    <TableCell>{dataset.size}</TableCell>
                    <TableCell>
                      <Chip
                        label={dataset.status}
                        color={getStatusColor(dataset.status)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      {new Date(dataset.created).toLocaleString()}
                    </TableCell>
                    <TableCell>
                      {dataset.status === 'processing' && (
                        <Button
                          size="small"
                          startIcon={<StopIcon />}
                          onClick={() => console.log(`Stop processing ${dataset.name}`)}
                          color="error"
                        >
                          Stop
                        </Button>
                      )}
                      {dataset.status === 'completed' && (
                        <Button
                          size="small"
                          startIcon={<PlayIcon />}
                          onClick={() => console.log(`Process ${dataset.name}`)}
                        >
                          Process
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default GalaxyIntegration;
