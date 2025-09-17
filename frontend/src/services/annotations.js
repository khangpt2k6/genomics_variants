import api from './api';

export const annotationsApi = {
  // Get annotation sources
  getSources: async () => {
    const response = await api.get('/annotations/sources/');
    return response.data;
  },

  // Get annotation jobs
  getJobs: async (filters = {}) => {
    const response = await api.get('/annotations/jobs/', { params: filters });
    return response.data;
  },

  // Create annotation job
  createJob: async (data) => {
    const response = await api.post('/annotations/jobs/', data);
    return response.data;
  },

  // Start annotation job
  startJob: async (id) => {
    const response = await api.post(`/annotations/jobs/${id}/start/`);
    return response.data;
  },

  // Cancel annotation job
  cancelJob: async (id) => {
    const response = await api.post(`/annotations/jobs/${id}/cancel/`);
    return response.data;
  },

  // Get job progress
  getJobProgress: async (id) => {
    const response = await api.get(`/annotations/jobs/${id}/progress/`);
    return response.data;
  },

  // Get variant annotations
  getVariantAnnotations: async (filters = {}) => {
    const response = await api.get('/annotations/variant-annotations/', { params: filters });
    return response.data;
  },

  // Get annotations by variant
  getByVariant: async (variantId) => {
    const response = await api.get('/annotations/variant-annotations/by_variant/', {
      params: { variant_id: variantId }
    });
    return response.data;
  },

  // Get annotations by source
  getBySource: async (source) => {
    const response = await api.get('/annotations/variant-annotations/by_source/', {
      params: { source }
    });
    return response.data;
  },

  // Get annotation statistics
  getStatistics: async (filters = {}) => {
    const response = await api.get('/annotations/variant-annotations/statistics/', { params: filters });
    return response.data;
  },

  // Get ClinVar annotations
  getClinVarAnnotations: async (filters = {}) => {
    const response = await api.get('/annotations/clinvar/', { params: filters });
    return response.data;
  },

  // Get COSMIC annotations
  getCOSMICAnnotations: async (filters = {}) => {
    const response = await api.get('/annotations/cosmic/', { params: filters });
    return response.data;
  },

  // Get CIViC annotations
  getCIViCAnnotations: async (filters = {}) => {
    const response = await api.get('/annotations/civic/', { params: filters });
    return response.data;
  },
};
