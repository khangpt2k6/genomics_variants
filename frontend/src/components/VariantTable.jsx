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
import PropTypes from 'prop-types';

import { 
  IMPACT_COLORS, 
  TABLE_CONFIG, 
  FREQUENCY_CONFIG,
  ERROR_MESSAGES 
} from '../constants';
import { formatFrequency, formatQualityScore } from '../utils';

/**
 * VariantTable component for displaying genetic variants in a table format.
 * 
 * @param {Object} props - Component props
 * @param {Array} props.variants - Array of variant objects
 * @param {boolean} props.loading - Loading state
 * @param {Error} props.error - Error object
 * @param {Function} props.onPageChange - Page change handler
 * @param {number} props.currentPage - Current page number
 * @param {number} props.totalPages - Total number of pages
 */
const VariantTable = ({
  variants = [],
  loading = false,
  error,
  onPageChange,
  currentPage = 1,
  totalPages = 1,
}) => {
  const navigate = useNavigate();

  const getImpactColor = (impact) => {
    return IMPACT_COLORS[impact] || 'default';
  };

  if (error) {
    return (
      <Box sx={{ p: 3, textAlign: 'center' }}>
        <Typography color="error">
          {ERROR_MESSAGES.LOADING_VARIANTS}: {error.message}
        </Typography>
      </Box>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ maxHeight: TABLE_CONFIG.MAX_HEIGHT }}>
      <Table stickyHeader={TABLE_CONFIG.STICKY_HEADER}>
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
            [...Array(TABLE_CONFIG.SKELETON_ROWS)].map((_, index) => (
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
                    {formatQualityScore(variant.quality_score)}
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
          count={totalPages * TABLE_CONFIG.ROWS_PER_PAGE}
          page={currentPage - 1}
          onPageChange={(_, page) => onPageChange(page + 1)}
          rowsPerPage={TABLE_CONFIG.ROWS_PER_PAGE}
          rowsPerPageOptions={[20, 50, 100]}
          labelRowsPerPage="Rows per page:"
        />
      )}
    </TableContainer>
  );
};

VariantTable.propTypes = {
  variants: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    chromosome: PropTypes.string.isRequired,
    position: PropTypes.number.isRequired,
    reference_allele: PropTypes.string.isRequired,
    alternate_allele: PropTypes.string.isRequired,
    gene_symbol: PropTypes.string,
    consequence: PropTypes.string,
    impact: PropTypes.oneOf(['HIGH', 'MODERATE', 'LOW', 'MODIFIER']),
    gnomad_af: PropTypes.number,
    quality_score: PropTypes.number,
  })).isRequired,
  loading: PropTypes.bool,
  error: PropTypes.instanceOf(Error),
  onPageChange: PropTypes.func.isRequired,
  currentPage: PropTypes.number,
  totalPages: PropTypes.number,
};

export default VariantTable;
