import React from 'react';
import {
  Grid,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Box,
  Chip,
  Stack,
  Typography,
} from '@mui/material';

const VariantFiltersPanel = ({
  filters,
  onFilterChange,
}) => {
  const handleFilterChange = (field, value) => {
    onFilterChange({ [field]: value || undefined });
  };

  const clearFilters = () => {
    onFilterChange({
      chromosome: undefined,
      gene_symbol: undefined,
      variant_id: undefined,
      position_min: undefined,
      position_max: undefined,
      quality_min: undefined,
      quality_max: undefined,
      impact: undefined,
      consequence: undefined,
      gnomad_af_min: undefined,
      gnomad_af_max: undefined,
      has_clinical_significance: undefined,
      clinical_significance: undefined,
      has_drug_response: undefined,
      drug_name: undefined,
      has_cosmic_data: undefined,
      search: undefined,
    });
  };

  const activeFilters = Object.entries(filters).filter(
    ([key, value]) => 
      value !== undefined && 
      value !== '' && 
      value !== 1 && 
      !['page', 'page_size', 'ordering'].includes(key)
  );

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">Filters</Typography>
        <Box>
          {activeFilters.length > 0 && (
            <Chip
              label={`${activeFilters.length} active`}
              color="primary"
              size="small"
              sx={{ mr: 1 }}
            />
          )}
          <Button size="small" onClick={clearFilters}>
            Clear All
          </Button>
        </Box>
      </Box>

      <Grid container spacing={2}>
        {/* Basic Filters */}
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            label="Chromosome"
            value={filters.chromosome || ''}
            onChange={(e) => handleFilterChange('chromosome', e.target.value)}
            size="small"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            label="Gene Symbol"
            value={filters.gene_symbol || ''}
            onChange={(e) => handleFilterChange('gene_symbol', e.target.value)}
            size="small"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            label="Variant ID"
            value={filters.variant_id || ''}
            onChange={(e) => handleFilterChange('variant_id', e.target.value)}
            size="small"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth size="small">
            <InputLabel>Impact</InputLabel>
            <Select
              value={filters.impact || ''}
              onChange={(e) => handleFilterChange('impact', e.target.value)}
              label="Impact"
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="HIGH">High</MenuItem>
              <MenuItem value="MODERATE">Moderate</MenuItem>
              <MenuItem value="LOW">Low</MenuItem>
              <MenuItem value="MODIFIER">Modifier</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        {/* Position Range */}
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            label="Min Position"
            type="number"
            value={filters.position_min || ''}
            onChange={(e) => handleFilterChange('position_min', parseInt(e.target.value) || undefined)}
            size="small"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            label="Max Position"
            type="number"
            value={filters.position_max || ''}
            onChange={(e) => handleFilterChange('position_max', parseInt(e.target.value) || undefined)}
            size="small"
          />
        </Grid>

        {/* Quality Range */}
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            label="Min Quality"
            type="number"
            value={filters.quality_min || ''}
            onChange={(e) => handleFilterChange('quality_min', parseFloat(e.target.value) || undefined)}
            size="small"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            label="Max Quality"
            type="number"
            value={filters.quality_max || ''}
            onChange={(e) => handleFilterChange('quality_max', parseFloat(e.target.value) || undefined)}
            size="small"
          />
        </Grid>

        {/* Frequency Range */}
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            label="Min gnomAD AF"
            type="number"
            inputProps={{ step: 0.0001, min: 0, max: 1 }}
            value={filters.gnomad_af_min || ''}
            onChange={(e) => handleFilterChange('gnomad_af_min', parseFloat(e.target.value) || undefined)}
            size="small"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            label="Max gnomAD AF"
            type="number"
            inputProps={{ step: 0.0001, min: 0, max: 1 }}
            value={filters.gnomad_af_max || ''}
            onChange={(e) => handleFilterChange('gnomad_af_max', parseFloat(e.target.value) || undefined)}
            size="small"
          />
        </Grid>

        {/* Clinical Significance */}
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth size="small">
            <InputLabel>Clinical Significance</InputLabel>
            <Select
              value={filters.clinical_significance || ''}
              onChange={(e) => handleFilterChange('clinical_significance', e.target.value)}
              label="Clinical Significance"
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="pathogenic">Pathogenic</MenuItem>
              <MenuItem value="likely_pathogenic">Likely Pathogenic</MenuItem>
              <MenuItem value="uncertain_significance">Uncertain Significance</MenuItem>
              <MenuItem value="likely_benign">Likely Benign</MenuItem>
              <MenuItem value="benign">Benign</MenuItem>
              <MenuItem value="conflicting">Conflicting</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        {/* Drug Response */}
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            label="Drug Name"
            value={filters.drug_name || ''}
            onChange={(e) => handleFilterChange('drug_name', e.target.value)}
            size="small"
          />
        </Grid>

        {/* Boolean Filters */}
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth size="small">
            <InputLabel>Has Clinical Data</InputLabel>
            <Select
              value={filters.has_clinical_significance === undefined ? '' : filters.has_clinical_significance}
              onChange={(e) => handleFilterChange('has_clinical_significance', e.target.value === '' ? undefined : e.target.value)}
              label="Has Clinical Data"
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value={true}>Yes</MenuItem>
              <MenuItem value={false}>No</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth size="small">
            <InputLabel>Has Drug Data</InputLabel>
            <Select
              value={filters.has_drug_response === undefined ? '' : filters.has_drug_response}
              onChange={(e) => handleFilterChange('has_drug_response', e.target.value === '' ? undefined : e.target.value)}
              label="Has Drug Data"
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value={true}>Yes</MenuItem>
              <MenuItem value={false}>No</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth size="small">
            <InputLabel>Has COSMIC Data</InputLabel>
            <Select
              value={filters.has_cosmic_data === undefined ? '' : filters.has_cosmic_data}
              onChange={(e) => handleFilterChange('has_cosmic_data', e.target.value === '' ? undefined : e.target.value)}
              label="Has COSMIC Data"
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value={true}>Yes</MenuItem>
              <MenuItem value={false}>No</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>
    </Box>
  );
};

export default VariantFiltersPanel;
