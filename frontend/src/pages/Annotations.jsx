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
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { annotationsApi } from '../services/annotations';

const Annotations = () => {
  const { data: jobs, isLoading: jobsLoading, refetch: refetchJobs } = useQuery({
    queryKey: ['annotationJobs'],
    queryFn: () => annotationsApi.getJobs()
  });

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['annotationStatistics'],
    queryFn: () => annotationsApi.getStatistics()
  });

  const handleStartJob = async (jobId) => {
    try {
      await annotationsApi.startJob(jobId);
      refetchJobs();
    } catch (error) {
      console.error('Failed to start job:', error);
    }
  };

  const handleCancelJob = async (jobId) => {
    try {
      await annotationsApi.cancelJob(jobId);
      refetchJobs();
    } catch (error) {
      console.error('Failed to cancel job:', error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'running':
        return 'info';
      case 'failed':
        return 'error';
      case 'cancelled':
        return 'default';
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
          Annotations
        </Typography>
        <Button
          variant="contained"
          startIcon={<PlayIcon />}
          onClick={() => {
            // Implement create new annotation job
            console.log('Create new annotation job');
          }}
        >
          New Annotation Job
        </Button>
      </Box>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="primary">
                {stats?.total_annotations || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total Annotations
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="success.main">
                {stats?.successful_annotations || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Successful
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="error.main">
                {stats?.failed_annotations || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Failed
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="info.main">
                {stats?.success_rate || 0}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Success Rate
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Annotation Jobs */}
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              Annotation Jobs
            </Typography>
            <Button
              startIcon={<RefreshIcon />}
              onClick={() => refetchJobs()}
            >
              Refresh
            </Button>
          </Box>

          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Job ID</TableCell>
                  <TableCell>Source</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Progress</TableCell>
                  <TableCell>Variants</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {jobsLoading ? (
                  <TableRow>
                    <TableCell colSpan={7} sx={{ textAlign: 'center', py: 4 }}>
                      Loading jobs...
                    </TableCell>
                  </TableRow>
                ) : jobs?.results?.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={7} sx={{ textAlign: 'center', py: 4 }}>
                      <Typography color="text.secondary">
                        No annotation jobs found
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  jobs?.results?.map((job) => (
                    <TableRow key={job.id}>
                      <TableCell>
                        <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                          {job.job_id}
                        </Typography>
                      </TableCell>
                      <TableCell>{job.source_name}</TableCell>
                      <TableCell>
                        <Chip
                          label={job.status}
                          color={getStatusColor(job.status)}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Box sx={{ width: 100, height: 8, bgcolor: 'grey.200', borderRadius: 1 }}>
                            <Box
                              sx={{
                                width: `${job.progress_percentage}%`,
                                height: '100%',
                                bgcolor: job.status === 'failed' ? 'error.main' : 'primary.main',
                                borderRadius: 1,
                              }}
                            />
                          </Box>
                          <Typography variant="caption">
                            {job.progress_percentage}%
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>
                        {job.processed_count} / {job.variant_count}
                      </TableCell>
                      <TableCell>
                        {new Date(job.created_at).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        {job.status === 'pending' && (
                          <Button
                            size="small"
                            startIcon={<PlayIcon />}
                            onClick={() => handleStartJob(job.id)}
                          >
                            Start
                          </Button>
                        )}
                        {(job.status === 'running' || job.status === 'pending') && (
                          <Button
                            size="small"
                            startIcon={<StopIcon />}
                            onClick={() => handleCancelJob(job.id)}
                            color="error"
                          >
                            Cancel
                          </Button>
                        )}
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Annotations;
