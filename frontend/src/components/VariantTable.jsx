import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  Tooltip,
  TablePagination,
  Skeleton,
  Box,
  Typography,
} from '@mui/material';
import {
  Visibility as VisibilityIcon,
  Science as ScienceIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const VariantTable = ({
  variants,
  loading = false,
  error,
  onPageChange,
  currentPage,
  totalPages,
}) => {
  const navigate = useNavigate();

  const getImpactColor = (impact) => {
    switch (impact) {
      case 'HIGH':
        return 'error';
      case 'MODERATE':
        return 'warning';
      case 'LOW':
        return 'info';
      case 'MODIFIER':
        return 'default';
      default:
        return 'default';
    }
  };

  const formatFrequency = (frequency) => {
    if (frequency === undefined || frequency === null) return 'N/A';
    return frequency < 0.001 ? frequency.toExponential(2) : frequency.toFixed(4);
  };

  if (error) {
    return (
      <Box sx={{ p: 3, textAlign: 'center' }}>
        <Typography color="error">
          Error loading variants: {error.message}
        </Typography>
      </Box>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ maxHeight: 600 }}>
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            <TableCell>Variant</TableCell>
            <TableCell>Gene</TableCell>
            <TableCell>Consequence</TableCell>
            <TableCell>Impact</TableCell>
            <TableCell>gnomAD AF</TableCell>
            <TableCell>Quality</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {loading ? (
            [...Array(10)].map((_, index) => (
              <TableRow key={index}>
                <TableCell><Skeleton variant="text" width={120} /></TableCell>
                <TableCell><Skeleton variant="text" width={80} /></TableCell>
                <TableCell><Skeleton variant="text" width={100} /></TableCell>
                <TableCell><Skeleton variant="text" width={60} /></TableCell>
                <TableCell><Skeleton variant="text" width={60} /></TableCell>
                <TableCell><Skeleton variant="text" width={60} /></TableCell>
                <TableCell><Skeleton variant="text" width={40} /></TableCell>
              </TableRow>
            ))
          ) : variants.length === 0 ? (
            <TableRow>
              <TableCell colSpan={7} sx={{ textAlign: 'center', py: 4 }}>
                <Typography color="text.secondary">
                  No variants found
                </Typography>
              </TableCell>
            </TableRow>
          ) : (
            variants.map((variant) => (
              <TableRow key={variant.id} hover>
                <TableCell>
                  <Box>
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                      {variant.chromosome}:{variant.position}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {variant.reference_allele} → {variant.alternate_allele}
                    </Typography>
                  </Box>
                </TableCell>
                <TableCell>
                  {variant.gene_symbol || (
                    <Typography color="text.secondary" variant="body2">
                      N/A
                    </Typography>
                  )}
                </TableCell>
                <TableCell>
                  <Typography variant="body2" sx={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {variant.consequence || 'N/A'}
                  </Typography>
                </TableCell>
                <TableCell>
                  {variant.impact ? (
                    <Chip
                      label={variant.impact}
                      size="small"
                      color={getImpactColor(variant.impact)}
                      variant="outlined"
                    />
                  ) : (
                    <Typography color="text.secondary" variant="body2">
                      N/A
                    </Typography>
                  )}
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {formatFrequency(variant.gnomad_af)}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {variant.quality_score ? variant.quality_score.toFixed(2) : 'N/A'}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Tooltip title="View Details">
                    <IconButton
                      size="small"
                      onClick={() => navigate(`/variants/${variant.id}`)}
                    >
                      <VisibilityIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
      
      {!loading && variants.length > 0 && (
        <TablePagination
          component="div"
          count={totalPages * 20} // Approximate total count
          page={currentPage - 1}
          onPageChange={(_, page) => onPageChange(page + 1)}
          rowsPerPage={20}
          rowsPerPageOptions={[20, 50, 100]}
          labelRowsPerPage="Rows per page:"
        />
      )}
    </TableContainer>
  );
};

export default VariantTable;
