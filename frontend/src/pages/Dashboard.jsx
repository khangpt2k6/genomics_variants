import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Paper,
} from '@mui/material';
import {
  Science as ScienceIcon,
  Assignment as AssignmentIcon,
  CloudUpload as CloudUploadIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { variantsApi } from '../services/variants';
import { annotationsApi } from '../services/annotations';
import StatCard from '../components/StatCard';
import VariantChart from '../components/VariantChart';
import RecentVariants from '../components/RecentVariants';

const Dashboard = () => {
  const { data: variantStats, isLoading: variantStatsLoading } = useQuery({
    queryKey: ['variantStatistics'],
    queryFn: () => variantsApi.getStatistics()
  });

  const { data: annotationStats, isLoading: annotationStatsLoading } = useQuery({
    queryKey: ['annotationStatistics'],
    queryFn: () => annotationsApi.getStatistics()
  });

  const { data: recentVariants, isLoading: recentVariantsLoading } = useQuery({
    queryKey: ['recentVariants'],
    queryFn: () => variantsApi.getVariants({ page_size: 5, ordering: '-created_at' })
  });

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        Dashboard
      </Typography>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Variants"
            value={variantStats?.total_variants || 0}
            icon={<ScienceIcon />}
            color="primary"
            loading={variantStatsLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Pathogenic Variants"
            value={variantStats?.pathogenic_count || 0}
            icon={<TrendingUpIcon />}
            color="error"
            loading={variantStatsLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Drug Targets"
            value={variantStats?.drug_target_count || 0}
            icon={<AssignmentIcon />}
            color="success"
            loading={variantStatsLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Annotations"
            value={annotationStats?.total_annotations || 0}
            icon={<CloudUploadIcon />}
            color="info"
            loading={annotationStatsLoading}
          />
        </Grid>
      </Grid>

      {/* Charts and Recent Data */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Variant Distribution
              </Typography>
              <VariantChart data={variantStats} loading={variantStatsLoading} />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Variants
              </Typography>
              <RecentVariants 
                variants={recentVariants?.results || []} 
                loading={recentVariantsLoading} 
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
