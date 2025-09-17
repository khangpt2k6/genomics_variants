import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterListIcon,
  Download as DownloadIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { variantsApi } from '../services/variants';
import VariantTable from '../components/VariantTable';
import VariantFiltersPanel from '../components/VariantFiltersPanel';

const Variants = () => {
  const [filters, setFilters] = useState({
    page: 1,
    page_size: 20,
    ordering: '-created_at',
  });
  const [showFilters, setShowFilters] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['variants', filters],
    queryFn: () => variantsApi.getVariants(filters),
    keepPreviousData: true,
  });

  const handleSearch = () => {
    setFilters(prev => ({
      ...prev,
      search: searchTerm || undefined,
      page: 1,
    }));
  };

  const handleFilterChange = (newFilters) => {
    setFilters(prev => ({
      ...prev,
      ...newFilters,
      page: 1,
    }));
  };

  const handlePageChange = (page) => {
    setFilters(prev => ({
      ...prev,
      page,
    }));
  };

  const handleExport = () => {
    // Implement export functionality
    console.log('Export variants');
  };

  const activeFiltersCount = Object.values(filters).filter(
    value => value !== undefined && value !== '' && value !== 1
  ).length - 2; // Subtract page and page_size

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Variants
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<FilterListIcon />}
            onClick={() => setShowFilters(!showFilters)}
            color={showFilters ? 'primary' : 'inherit'}
          >
            Filters {activeFiltersCount > 0 && `(${activeFiltersCount})`}
          </Button>
          <Button
            variant="outlined"
            startIcon={<DownloadIcon />}
            onClick={handleExport}
          >
            Export
          </Button>
          <Tooltip title="Refresh">
            <IconButton onClick={() => refetch()}>
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Search Bar */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={8}>
              <TextField
                fullWidth
                placeholder="Search variants by ID, gene, consequence, or phenotype..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                InputProps={{
                  startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <Button
                fullWidth
                variant="contained"
                onClick={handleSearch}
                sx={{ height: '56px' }}
              >
                Search
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Filters Panel */}
      {showFilters && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <VariantFiltersPanel
              filters={filters}
              onFilterChange={handleFilterChange}
            />
          </CardContent>
        </Card>
      )}

      {/* Results Summary */}
      {data && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="text.secondary">
            Showing {data.results?.length || 0} of {data.count || 0} variants
            {data.next && ` (Page ${filters.page})`}
          </Typography>
        </Box>
      )}

      {/* Variants Table */}
      <Card>
        <CardContent sx={{ p: 0 }}>
          <VariantTable
            variants={data?.results || []}
            loading={isLoading}
            error={error}
            onPageChange={handlePageChange}
            currentPage={filters.page || 1}
            totalPages={data ? Math.ceil((data.count || 0) / (filters.page_size || 20)) : 1}
          />
        </CardContent>
      </Card>
    </Box>
  );
};

export default Variants;
