import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
} from '@mui/material';
import {
  Science as ScienceIcon,
  Assignment as AssignmentIcon,
  CloudUpload as CloudUploadIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import PropTypes from 'prop-types';

import { variantsApi } from '../services/variants';
import { annotationsApi } from '../services/annotations';
import StatCard from '../components/StatCard';
import VariantChart from '../components/VariantChart';
import RecentVariants from '../components/RecentVariants';
import { 
  QUERY_KEYS, 
  THEME, 
  PAGINATION,
  ANIMATION
} from '../constants';

/**
 * Dashboard component displaying variant statistics and recent data.
 * 
 * This component shows key metrics, charts, and recent variants
 * to provide an overview of the variant database.
 */
const Dashboard = () => {
  const { data: variantStats, isLoading: variantStatsLoading } = useQuery({
    queryKey: [QUERY_KEYS.VARIANT_STATISTICS],
    queryFn: () => variantsApi.getStatistics()
  });

  const { data: annotationStats, isLoading: annotationStatsLoading } = useQuery({
    queryKey: [QUERY_KEYS.ANNOTATION_STATISTICS],
    queryFn: () => annotationsApi.getStatistics()
  });

  const { data: recentVariants, isLoading: recentVariantsLoading } = useQuery({
    queryKey: [QUERY_KEYS.RECENT_VARIANTS],
    queryFn: () => variantsApi.getVariants({ 
      page_size: 5, 
      ordering: '-created_at' 
    })
  });

  return (
    <Box sx={{ background: 'transparent' }}>
      <Typography 
        variant="h4" 
        gutterBottom 
        sx={{ 
          mb: 4,
          fontWeight: 700,
          background: 'linear-gradient(135deg, #E91E63, #9C27B0)',
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          textShadow: '0 2px 4px rgba(233, 30, 99, 0.2)',
        }}
      >
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
          <Card
            sx={{
              background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 187, 208, 0.1) 50%, rgba(156, 39, 176, 0.1) 100%)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(233, 30, 99, 0.1)',
              borderRadius: 3,
              boxShadow: '0 8px 32px rgba(233, 30, 99, 0.15)',
              transition: 'all 0.3s ease',
              '&:hover': {
                background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 187, 208, 0.15) 50%, rgba(156, 39, 176, 0.15) 100%)',
                borderColor: 'rgba(233, 30, 99, 0.2)',
                transform: 'translateY(-4px)',
                boxShadow: '0 12px 48px rgba(233, 30, 99, 0.25)',
              }
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Typography 
                variant="h6" 
                gutterBottom
                sx={{
                  background: 'linear-gradient(135deg, #E91E63, #9C27B0)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  fontWeight: 600,
                  textShadow: '0 2px 4px rgba(233, 30, 99, 0.2)',
                  mb: 3
                }}
              >
                Variant Distribution
              </Typography>
              <VariantChart data={variantStats} loading={variantStatsLoading} />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card
            sx={{
              background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 187, 208, 0.1) 50%, rgba(156, 39, 176, 0.1) 100%)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(233, 30, 99, 0.1)',
              borderRadius: 3,
              boxShadow: '0 8px 32px rgba(233, 30, 99, 0.15)',
              transition: 'all 0.3s ease',
              '&:hover': {
                background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 187, 208, 0.15) 50%, rgba(156, 39, 176, 0.15) 100%)',
                borderColor: 'rgba(233, 30, 99, 0.2)',
                transform: 'translateY(-4px)',
                boxShadow: '0 12px 48px rgba(233, 30, 99, 0.25)',
              }
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Typography 
                variant="h6" 
                gutterBottom
                sx={{
                  background: 'linear-gradient(135deg, #E91E63, #9C27B0)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  fontWeight: 600,
                  textShadow: '0 2px 4px rgba(233, 30, 99, 0.2)',
                  mb: 3
                }}
              >
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

Dashboard.propTypes = {};

export default Dashboard;
