import React from 'react';
import {
  List,
  ListItem,
  ListItemText,
  Chip,
  Box,
  Typography,
  Skeleton,
} from '@mui/material';

const RecentVariants = ({ variants, loading = false }) => {
  if (loading) {
    return (
      <Box>
        {[...Array(5)].map((_, index) => (
          <Box key={index} sx={{ mb: 1 }}>
            <Skeleton variant="text" width="100%" height={40} />
          </Box>
        ))}
      </Box>
    );
  }

  if (variants.length === 0) {
    return (
      <Typography color="text.secondary" variant="body2">
        No recent variants found
      </Typography>
    );
  }

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

  return (
    <List dense>
      {variants.map((variant) => (
        <ListItem key={variant.id} sx={{ px: 0 }}>
          <ListItemText
            primary={
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Typography variant="body2" sx={{ fontWeight: 500 }}>
                  {variant.chromosome}:{variant.position} {variant.reference_allele}→{variant.alternate_allele}
                </Typography>
                {variant.impact && (
                  <Chip
                    label={variant.impact}
                    size="small"
                    color={getImpactColor(variant.impact)}
                    variant="outlined"
                  />
                )}
              </Box>
            }
            secondary={
              <Box>
                {variant.gene_symbol && (
                  <Typography variant="caption" color="text.secondary">
                    Gene: {variant.gene_symbol}
                  </Typography>
                )}
                {variant.consequence && (
                  <Typography variant="caption" color="text.secondary" sx={{ ml: 1 }}>
                    • {variant.consequence}
                  </Typography>
                )}
              </Box>
            }
          />
        </ListItem>
      ))}
    </List>
  );
};

export default RecentVariants;
