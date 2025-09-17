import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  Button,
  Tabs,
  Tab,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Divider,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Science as ScienceIcon,
  Assignment as AssignmentIcon,
  LocalHospital as LocalHospitalIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { variantsApi } from '../services/variants';

const VariantDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = React.useState(0);

  const { data: variant, isLoading, error } = useQuery({
    queryKey: ['variant', id],
    queryFn: () => variantsApi.getVariant(parseInt(id)),
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <Box>
        <Typography>Loading variant details...</Typography>
      </Box>
    );
  }

  if (error || !variant) {
    return (
      <Box>
        <Typography color="error">
          Error loading variant: {error?.message || 'Variant not found'}
        </Typography>
      </Box>
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

  const getSignificanceColor = (significance) => {
    switch (significance) {
      case 'pathogenic':
        return 'error';
      case 'likely_pathogenic':
        return 'warning';
      case 'uncertain_significance':
        return 'info';
      case 'likely_benign':
      case 'benign':
        return 'success';
      case 'conflicting':
        return 'secondary';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/variants')}
          sx={{ mr: 2 }}
        >
          Back to Variants
        </Button>
        <Typography variant="h4" sx={{ flexGrow: 1 }}>
          Variant Details
        </Typography>
      </Box>

      {/* Basic Information */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Basic Information
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Variant ID
                </Typography>
                <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
                  {variant.variant_id}
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Genomic Position
                </Typography>
                <Typography variant="body1">
                  {variant.chromosome}:{variant.position}
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Allele Change
                </Typography>
                <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
                  {variant.reference_allele} → {variant.alternate_allele}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Gene Symbol
                </Typography>
                <Typography variant="body1">
                  {variant.gene_symbol || 'N/A'}
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Consequence
                </Typography>
                <Typography variant="body1">
                  {variant.consequence || 'N/A'}
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Impact
                </Typography>
                {variant.impact ? (
                  <Chip
                    label={variant.impact}
                    color={getImpactColor(variant.impact)}
                    variant="outlined"
                  />
                ) : (
                  <Typography variant="body1">N/A</Typography>
                )}
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Tabs for detailed information */}
      <Card>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
            <Tab icon={<ScienceIcon />} label="Annotations" />
            <Tab icon={<LocalHospitalIcon />} label="Clinical Significance" />
            <Tab icon={<AssignmentIcon />} label="Drug Responses" />
            <Tab icon={<AssignmentIcon />} label="COSMIC Data" />
          </Tabs>
        </Box>

        <CardContent>
          {/* Annotations Tab */}
          {activeTab === 0 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Variant Annotations
              </Typography>
              {variant.annotations && variant.annotations.length > 0 ? (
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Annotation Type</TableCell>
                        <TableCell>Pathogenic</TableCell>
                        <TableCell>Drug Target</TableCell>
                        <TableCell>COSMIC Data</TableCell>
                        <TableCell>Pathogenicity Score</TableCell>
                        <TableCell>Drug Response Score</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {variant.annotations.map((annotation) => (
                        <TableRow key={annotation.id}>
                          <TableCell>{annotation.annotation_version}</TableCell>
                          <TableCell>
                            <Chip
                              label={annotation.is_pathogenic ? 'Yes' : 'No'}
                              color={annotation.is_pathogenic ? 'error' : 'default'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={annotation.is_drug_target ? 'Yes' : 'No'}
                              color={annotation.is_drug_target ? 'success' : 'default'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={annotation.has_cosmic_data ? 'Yes' : 'No'}
                              color={annotation.has_cosmic_data ? 'info' : 'default'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            {annotation.pathogenicity_score?.toFixed(3) || 'N/A'}
                          </TableCell>
                          <TableCell>
                            {annotation.drug_response_score?.toFixed(3) || 'N/A'}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Typography color="text.secondary">
                  No annotations available for this variant.
                </Typography>
              )}
            </Box>
          )}

          {/* Clinical Significance Tab */}
          {activeTab === 1 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Clinical Significance
              </Typography>
              {variant.clinical_significance && variant.clinical_significance.length > 0 ? (
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Significance</TableCell>
                        <TableCell>Review Status</TableCell>
                        <TableCell>ClinVar ID</TableCell>
                        <TableCell>Evidence Level</TableCell>
                        <TableCell>Phenotype</TableCell>
                        <TableCell>Review Date</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {variant.clinical_significance.map((cs) => (
                        <TableRow key={cs.id}>
                          <TableCell>
                            <Chip
                              label={cs.significance.replace('_', ' ').toUpperCase()}
                              color={getSignificanceColor(cs.significance)}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>{cs.review_status || 'N/A'}</TableCell>
                          <TableCell>{cs.clinvar_id || 'N/A'}</TableCell>
                          <TableCell>{cs.evidence_level || 'N/A'}</TableCell>
                          <TableCell>{cs.phenotype || 'N/A'}</TableCell>
                          <TableCell>{cs.review_date || 'N/A'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Typography color="text.secondary">
                  No clinical significance data available for this variant.
                </Typography>
              )}
            </Box>
          )}

          {/* Drug Responses Tab */}
          {activeTab === 2 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Drug Responses
              </Typography>
              {variant.drug_responses && variant.drug_responses.length > 0 ? (
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Drug Name</TableCell>
                        <TableCell>Response Type</TableCell>
                        <TableCell>Evidence Level</TableCell>
                        <TableCell>Evidence Direction</TableCell>
                        <TableCell>Cancer Type</TableCell>
                        <TableCell>Tissue Type</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {variant.drug_responses.map((dr) => (
                        <TableRow key={dr.id}>
                          <TableCell>{dr.drug_name}</TableCell>
                          <TableCell>{dr.response_type}</TableCell>
                          <TableCell>{dr.evidence_level}</TableCell>
                          <TableCell>{dr.evidence_direction}</TableCell>
                          <TableCell>{dr.cancer_type || 'N/A'}</TableCell>
                          <TableCell>{dr.tissue_type || 'N/A'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Typography color="text.secondary">
                  No drug response data available for this variant.
                </Typography>
              )}
            </Box>
          )}

          {/* COSMIC Data Tab */}
          {activeTab === 3 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                COSMIC Data
              </Typography>
              {variant.cosmic_data && variant.cosmic_data.length > 0 ? (
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>COSMIC ID</TableCell>
                        <TableCell>Primary Site</TableCell>
                        <TableCell>Histology</TableCell>
                        <TableCell>Mutation Frequency</TableCell>
                        <TableCell>Mutation Count</TableCell>
                        <TableCell>Sample Source</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {variant.cosmic_data.map((cosmic) => (
                        <TableRow key={cosmic.id}>
                          <TableCell>{cosmic.cosmic_id}</TableCell>
                          <TableCell>{cosmic.primary_site || 'N/A'}</TableCell>
                          <TableCell>{cosmic.primary_histology || 'N/A'}</TableCell>
                          <TableCell>{cosmic.mutation_frequency?.toFixed(4) || 'N/A'}</TableCell>
                          <TableCell>{cosmic.mutation_count || 'N/A'}</TableCell>
                          <TableCell>{cosmic.sample_source || 'N/A'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Typography color="text.secondary">
                  No COSMIC data available for this variant.
                </Typography>
              )}
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default VariantDetail;
