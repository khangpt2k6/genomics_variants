import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#E91E63', // Pink
      light: '#F8BBD9',
      dark: '#C2185B',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#9C27B0', // Purple
      light: '#E1BEE7',
      dark: '#7B1FA2',
      contrastText: '#ffffff',
    },
    error: {
      main: '#F44336',
      light: '#FFCDD2',
      dark: '#D32F2F',
    },
    warning: {
      main: '#FF9800',
      light: '#FFE0B2',
      dark: '#F57C00',
    },
    info: {
      main: '#2196F3',
      light: '#BBDEFB',
      dark: '#1976D2',
    },
    success: {
      main: '#4CAF50',
      light: '#C8E6C9',
      dark: '#388E3C',
    },
    background: {
      default: 'linear-gradient(135deg, #FCE4EC 0%, #F3E5F5 25%, #E8EAF6 50%, #FFF3E0 75%, #F1F8E9 100%)',
      paper: 'rgba(255, 255, 255, 0.9)',
    },
    text: {
      primary: '#333333',
      secondary: '#666666',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      background: 'linear-gradient(135deg, #E91E63, #9C27B0)',
      backgroundClip: 'text',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
    },
    h2: {
      fontWeight: 600,
      background: 'linear-gradient(135deg, #E91E63, #9C27B0)',
      backgroundClip: 'text',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
    },
    h3: {
      fontWeight: 600,
      background: 'linear-gradient(135deg, #E91E63, #9C27B0)',
      backgroundClip: 'text',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
    },
    h4: {
      fontWeight: 600,
      background: 'linear-gradient(135deg, #E91E63, #9C27B0)',
      backgroundClip: 'text',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 12,
  },
  shadows: [
    'none',
    '0 2px 4px rgba(233, 30, 99, 0.1)',
    '0 4px 8px rgba(233, 30, 99, 0.1)',
    '0 8px 16px rgba(233, 30, 99, 0.1)',
    '0 12px 24px rgba(233, 30, 99, 0.15)',
    '0 16px 32px rgba(233, 30, 99, 0.15)',
    '0 8px 32px rgba(233, 30, 99, 0.15)',
    '0 12px 48px rgba(233, 30, 99, 0.25)',
    '0 16px 64px rgba(233, 30, 99, 0.25)',
    '0 20px 80px rgba(233, 30, 99, 0.3)',
    '0 24px 96px rgba(233, 30, 99, 0.3)',
    '0 28px 112px rgba(233, 30, 99, 0.35)',
    '0 32px 128px rgba(233, 30, 99, 0.35)',
    '0 36px 144px rgba(233, 30, 99, 0.4)',
    '0 40px 160px rgba(233, 30, 99, 0.4)',
    '0 44px 176px rgba(233, 30, 99, 0.45)',
    '0 48px 192px rgba(233, 30, 99, 0.45)',
    '0 52px 208px rgba(233, 30, 99, 0.5)',
    '0 56px 224px rgba(233, 30, 99, 0.5)',
    '0 60px 240px rgba(233, 30, 99, 0.55)',
    '0 64px 256px rgba(233, 30, 99, 0.55)',
    '0 68px 272px rgba(233, 30, 99, 0.6)',
    '0 72px 288px rgba(233, 30, 99, 0.6)',
    '0 76px 304px rgba(233, 30, 99, 0.65)',
    '0 80px 320px rgba(233, 30, 99, 0.65)',
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          textTransform: 'none',
          fontWeight: 600,
          boxShadow: '0 4px 16px rgba(233, 30, 99, 0.2)',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 8px 24px rgba(233, 30, 99, 0.3)',
          },
        },
        contained: {
          background: 'linear-gradient(135deg, #E91E63, #9C27B0)',
          '&:hover': {
            background: 'linear-gradient(135deg, #C2185B, #7B1FA2)',
          },
        },
        outlined: {
          borderColor: 'rgba(233, 30, 99, 0.3)',
          color: '#E91E63',
          '&:hover': {
            borderColor: 'rgba(233, 30, 99, 0.5)',
            background: 'rgba(233, 30, 99, 0.05)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 187, 208, 0.1) 50%, rgba(156, 39, 176, 0.1) 100%)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(233, 30, 99, 0.1)',
          borderRadius: 16,
          boxShadow: '0 8px 32px rgba(233, 30, 99, 0.15)',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0 12px 48px rgba(233, 30, 99, 0.25)',
            borderColor: 'rgba(233, 30, 99, 0.2)',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 12,
            '& fieldset': {
              borderColor: 'rgba(233, 30, 99, 0.2)',
            },
            '&:hover fieldset': {
              borderColor: 'rgba(233, 30, 99, 0.4)',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#E91E63',
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(252, 228, 236, 0.8) 100%)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(233, 30, 99, 0.1)',
          boxShadow: '0 4px 16px rgba(233, 30, 99, 0.1)',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(252, 228, 236, 0.8) 100%)',
          backdropFilter: 'blur(20px)',
          borderRight: '1px solid rgba(233, 30, 99, 0.1)',
          boxShadow: '8px 0 24px rgba(233, 30, 99, 0.1)',
        },
      },
    },
  },
});

export default theme;
