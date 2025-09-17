import api from './api';

export const variantsApi = {
  // Get variants with filters
  getVariants: async (filters = {}) => {
    const response = await api.get('/variants/', { params: filters });
    return response.data;
  },

  // Get single variant
  getVariant: async (id) => {
    const response = await api.get(`/variants/${id}/`);
    return response.data;
  },

  // Get variant statistics
  getStatistics: async (filters = {}) => {
    const response = await api.get('/variants/statistics/', { params: filters });
    return response.data;
  },

  // Search variants by gene
  searchByGene: async (gene, filters = {}) => {
    const response = await api.get('/variants/search_by_gene/', { 
      params: { gene, ...filters } 
    });
    return response.data;
  },

  // Get variant annotations
  getAnnotations: async (id) => {
    const response = await api.get(`/variants/${id}/annotations/`);
    return response.data;
  },

  // Get variant clinical significance
  getClinicalSignificance: async (id) => {
    const response = await api.get(`/variants/${id}/clinical_significance/`);
    return response.data;
  },

  // Get variant drug responses
  getDrugResponses: async (id) => {
    const response = await api.get(`/variants/${id}/drug_responses/`);
    return response.data;
  },

  // Get variant COSMIC data
  getCOSMICData: async (id) => {
    const response = await api.get(`/variants/${id}/cosmic_data/`);
    return response.data;
  },
};
