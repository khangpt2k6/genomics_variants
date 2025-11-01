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
  DEFAULT_PAGE_SIZE: 100,
  PAGE_SIZE_OPTIONS: [50, 100, 500, 1000, 5000],
  MAX_PAGE_SIZE: 10000,
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
    PRIMARY: '#E91E63', // Pink primary
    SECONDARY: '#9C27B0', // Purple secondary
    SUCCESS: '#4CAF50',
    ERROR: '#F44336',
    WARNING: '#FF9800',
    INFO: '#2196F3',
    ACCENT: '#FF4081', // Bright pink accent
    LIGHT_PINK: '#FCE4EC',
    LIGHT_PURPLE: '#F3E5F5',
  },
  GRADIENTS: {
    BACKGROUND: 'linear-gradient(135deg, #FCE4EC 0%, #F3E5F5 25%, #E8EAF6 50%, #FFF3E0 75%, #F1F8E9 100%)',
    PRIMARY: 'linear-gradient(135deg, #E91E63 0%, #9C27B0 100%)',
    SECONDARY: 'linear-gradient(135deg, #FF4081 0%, #E91E63 100%)',
    CARD: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 187, 208, 0.1) 50%, rgba(156, 39, 176, 0.1) 100%)',
    TEXT: 'linear-gradient(135deg, #E91E63, #9C27B0)',
    HERO: 'linear-gradient(135deg, #FCE4EC 0%, #F3E5F5 50%, #E8EAF6 100%)',
  },
  SHADOWS: {
    CARD: '0 8px 32px rgba(233, 30, 99, 0.15)',
    CARD_HOVER: '0 12px 48px rgba(233, 30, 99, 0.25)',
    TEXT: '0 2px 4px rgba(233, 30, 99, 0.2)',
    BUTTON: '0 4px 16px rgba(233, 30, 99, 0.2)',
    BUTTON_HOVER: '0 8px 24px rgba(233, 30, 99, 0.3)',
  },
  BORDERS: {
    CARD: '1px solid rgba(233, 30, 99, 0.1)',
    CARD_HOVER: '1px solid rgba(233, 30, 99, 0.2)',
    INPUT: '1px solid rgba(233, 30, 99, 0.3)',
  },
  BACKDROP: {
    BLUR: 'blur(20px)',
    OPACITY: 'rgba(255, 255, 255, 0.8)',
    OPACITY_HOVER: 'rgba(255, 255, 255, 0.9)',
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
