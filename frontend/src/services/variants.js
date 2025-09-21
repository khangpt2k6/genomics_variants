/**
 * Variants API service.
 * 
 * This module provides methods for interacting with the variants API endpoints,
 * including CRUD operations, filtering, and related data retrieval.
 */

import api, { retryRequest } from './api';
import { PAGINATION } from '../constants';
import { getErrorMessage } from '../utils';

/**
 * Variants API service object containing all variant-related API methods.
 */
export const variantsApi = {
  /**
   * Get variants with optional filters and pagination.
   * @param {Object} filters - Query parameters for filtering
   * @param {number} filters.page - Page number
   * @param {number} filters.page_size - Number of items per page
   * @param {string} filters.search - Search term
   * @param {string} filters.ordering - Ordering field
   * @param {string} filters.gene_symbol - Filter by gene symbol
   * @param {string} filters.impact - Filter by impact level
   * @param {string} filters.chromosome - Filter by chromosome
   * @returns {Promise<Object>} Paginated variants response
   */
  getVariants: async (filters = {}) => {
    try {
      const params = {
        page_size: PAGINATION.DEFAULT_PAGE_SIZE,
        ...filters,
      };
      
      const response = await api.get('/variants/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching variants:', getErrorMessage(error));
      throw error;
    }
  },

  /**
   * Get a single variant by ID.
   * @param {string|number} id - Variant ID
   * @returns {Promise<Object>} Variant data
   */
  getVariant: async (id) => {
    try {
      const response = await api.get(`/variants/${id}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching variant ${id}:`, getErrorMessage(error));
      throw error;
    }
  },

  /**
   * Get variant statistics.
   * @param {Object} filters - Optional filters for statistics
   * @returns {Promise<Object>} Statistics data
   */
  getStatistics: async (filters = {}) => {
    try {
      const response = await api.get('/variants/statistics/', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Error fetching variant statistics:', getErrorMessage(error));
      throw error;
    }
  },

  /**
   * Search variants by gene symbol.
   * @param {string} gene - Gene symbol to search for
   * @param {Object} filters - Additional filters
   * @returns {Promise<Object>} Search results
   */
  searchByGene: async (gene, filters = {}) => {
    try {
      if (!gene || gene.trim() === '') {
        throw new Error('Gene symbol is required for search');
      }
      
      const response = await api.get('/variants/search_by_gene/', { 
        params: { gene: gene.trim(), ...filters } 
      });
      return response.data;
    } catch (error) {
      console.error(`Error searching variants by gene ${gene}:`, getErrorMessage(error));
      throw error;
    }
  },

  /**
   * Get variant annotations.
   * @param {string|number} id - Variant ID
   * @returns {Promise<Array>} Annotations data
   */
  getAnnotations: async (id) => {
    try {
      const response = await api.get(`/variants/${id}/annotations/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching annotations for variant ${id}:`, getErrorMessage(error));
      throw error;
    }
  },

  /**
   * Get variant clinical significance data.
   * @param {string|number} id - Variant ID
   * @returns {Promise<Array>} Clinical significance data
   */
  getClinicalSignificance: async (id) => {
    try {
      const response = await api.get(`/variants/${id}/clinical_significance/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching clinical significance for variant ${id}:`, getErrorMessage(error));
      throw error;
    }
  },

  /**
   * Get variant drug response data.
   * @param {string|number} id - Variant ID
   * @returns {Promise<Array>} Drug response data
   */
  getDrugResponses: async (id) => {
    try {
      const response = await api.get(`/variants/${id}/drug_responses/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching drug responses for variant ${id}:`, getErrorMessage(error));
      throw error;
    }
  },

  /**
   * Get variant COSMIC data.
   * @param {string|number} id - Variant ID
   * @returns {Promise<Array>} COSMIC data
   */
  getCOSMICData: async (id) => {
    try {
      const response = await api.get(`/variants/${id}/cosmic_data/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching COSMIC data for variant ${id}:`, getErrorMessage(error));
      throw error;
    }
  },

  /**
   * Create a new variant.
   * @param {Object} variantData - Variant data
   * @returns {Promise<Object>} Created variant
   */
  createVariant: async (variantData) => {
    try {
      const response = await api.post('/variants/', variantData);
      return response.data;
    } catch (error) {
      console.error('Error creating variant:', getErrorMessage(error));
      throw error;
    }
  },

  /**
   * Update an existing variant.
   * @param {string|number} id - Variant ID
   * @param {Object} variantData - Updated variant data
   * @returns {Promise<Object>} Updated variant
   */
  updateVariant: async (id, variantData) => {
    try {
      const response = await api.put(`/variants/${id}/`, variantData);
      return response.data;
    } catch (error) {
      console.error(`Error updating variant ${id}:`, getErrorMessage(error));
      throw error;
    }
  },

  /**
   * Delete a variant.
   * @param {string|number} id - Variant ID
   * @returns {Promise<void>}
   */
  deleteVariant: async (id) => {
    try {
      await api.delete(`/variants/${id}/`);
    } catch (error) {
      console.error(`Error deleting variant ${id}:`, getErrorMessage(error));
      throw error;
    }
  },

  /**
   * Bulk create variants from VCF data.
   * @param {Array} variantsData - Array of variant data
   * @returns {Promise<Object>} Bulk creation result
   */
  bulkCreateVariants: async (variantsData) => {
    try {
      const response = await api.post('/variants/bulk_create/', {
        variants: variantsData
      });
      return response.data;
    } catch (error) {
      console.error('Error bulk creating variants:', getErrorMessage(error));
      throw error;
    }
  },
};
