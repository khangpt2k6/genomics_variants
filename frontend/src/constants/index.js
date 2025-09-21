/**
 * Application constants and configuration values.
 * 
 * This file contains all the constant values used throughout the application
 * to ensure consistency and make maintenance easier.
 */

// =============================================================================
// API CONFIGURATION
// =============================================================================

export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // 1 second
};

// =============================================================================
// PAGINATION
// =============================================================================

export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [20, 50, 100],
  MAX_PAGE_SIZE: 100,
};

// =============================================================================
// VARIANT IMPACT COLORS
// =============================================================================

export const IMPACT_COLORS = {
  HIGH: 'error',
  MODERATE: 'warning',
  LOW: 'info',
  MODIFIER: 'default',
};

// =============================================================================
// TABLE CONFIGURATION
// =============================================================================

export const TABLE_CONFIG = {
  MAX_HEIGHT: 600,
  STICKY_HEADER: true,
  ROWS_PER_PAGE: 20,
  SKELETON_ROWS: 10,
};

// =============================================================================
// FREQUENCY FORMATTING
// =============================================================================

export const FREQUENCY_CONFIG = {
  SMALL_NUMBER_THRESHOLD: 0.001,
  DECIMAL_PLACES: 4,
  EXPONENTIAL_DECIMAL_PLACES: 2,
};

// =============================================================================
// UI THEMES
// =============================================================================

export const THEME = {
  COLORS: {
    PRIMARY: '#1976d2',
    SECONDARY: '#dc004e',
    SUCCESS: '#2e7d32',
    ERROR: '#d32f2f',
    WARNING: '#ed6c02',
    INFO: '#0288d1',
  },
  GRADIENTS: {
    BACKGROUND: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0f0f0f 100%)',
    TEXT: 'linear-gradient(135deg, #ffffff, #b0b0b0)',
  },
  SHADOWS: {
    CARD: '0 8px 32px rgba(0, 0, 0, 0.3)',
    CARD_HOVER: '0 12px 48px rgba(0, 0, 0, 0.4)',
    TEXT: '0 2px 4px rgba(0, 0, 0, 0.3)',
  },
  BORDERS: {
    CARD: '1px solid rgba(255, 255, 255, 0.1)',
    CARD_HOVER: '1px solid rgba(255, 255, 255, 0.15)',
  },
  BACKDROP: {
    BLUR: 'blur(20px)',
    OPACITY: 'rgba(255, 255, 255, 0.06)',
    OPACITY_HOVER: 'rgba(255, 255, 255, 0.08)',
  },
};

// =============================================================================
// ANIMATION DURATIONS
// =============================================================================

export const ANIMATION = {
  FAST: '0.2s',
  NORMAL: '0.3s',
  SLOW: '0.5s',
  EASING: 'ease',
};

// =============================================================================
// ERROR MESSAGES
// =============================================================================

export const ERROR_MESSAGES = {
  LOADING_VARIANTS: 'Error loading variants',
  LOADING_ANNOTATIONS: 'Error loading annotations',
  LOADING_STATISTICS: 'Error loading statistics',
  NETWORK_ERROR: 'Network error. Please check your connection.',
  SERVER_ERROR: 'Server error. Please try again later.',
  UNAUTHORIZED: 'Unauthorized access. Please log in again.',
  NOT_FOUND: 'Resource not found.',
  VALIDATION_ERROR: 'Please check your input and try again.',
};

// =============================================================================
// SUCCESS MESSAGES
// =============================================================================

export const SUCCESS_MESSAGES = {
  DATA_LOADED: 'Data loaded successfully',
  ANNOTATION_UPDATED: 'Annotation updated successfully',
  VARIANT_CREATED: 'Variant created successfully',
  VARIANT_UPDATED: 'Variant updated successfully',
  VARIANT_DELETED: 'Variant deleted successfully',
};

// =============================================================================
// QUERY KEYS
// =============================================================================

export const QUERY_KEYS = {
  VARIANTS: 'variants',
  VARIANT_STATISTICS: 'variantStatistics',
  ANNOTATION_STATISTICS: 'annotationStatistics',
  RECENT_VARIANTS: 'recentVariants',
  VARIANT_DETAIL: 'variantDetail',
  CLINICAL_SIGNIFICANCE: 'clinicalSignificance',
  DRUG_RESPONSES: 'drugResponses',
  COSMIC_DATA: 'cosmicData',
  ANNOTATIONS: 'annotations',
};

// =============================================================================
// ROUTES
// =============================================================================

export const ROUTES = {
  DASHBOARD: '/',
  VARIANTS: '/variants',
  VARIANT_DETAIL: '/variants/:id',
  ANNOTATIONS: '/annotations',
  GALAXY: '/galaxy',
};

// =============================================================================
// LOCAL STORAGE KEYS
// =============================================================================

export const STORAGE_KEYS = {
  AUTH_TOKEN: 'authToken',
  USER_PREFERENCES: 'userPreferences',
  FILTERS: 'variantFilters',
  THEME: 'theme',
};
