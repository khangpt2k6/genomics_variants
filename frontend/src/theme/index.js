import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#000000', // Black
      light: '#333333',
      dark: '#000000',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#666666', // Dark gray
      light: '#999999',
      dark: '#333333',
      contrastText: '#ffffff',
    },
    error: {
      main: '#000000',
      light: '#333333',
      dark: '#000000',
    },
    warning: {
      main: '#666666',
      light: '#999999',
      dark: '#333333',
    },
    info: {
      main: '#000000',
      light: '#333333',
      dark: '#000000',
    },
    success: {
      main: '#000000',
      light: '#333333',
      dark: '#000000',
    },
    background: {
      default: '#ffffff',
      paper: '#ffffff',
    },
    text: {
      primary: '#000000',
      secondary: '#666666',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      color: '#000000',
    },
    h2: {
      fontWeight: 600,
      color: '#000000',
    },
    h3: {
      fontWeight: 600,
      color: '#000000',
    },
    h4: {
      fontWeight: 600,
      color: '#000000',
    },
    h5: {
      fontWeight: 600,
      color: '#000000',
    },
    h6: {
      fontWeight: 600,
      color: '#000000',
    },
  },
  shape: {
    borderRadius: 4,
  },
  shadows: [
    'none',
    '0 1px 2px rgba(0, 0, 0, 0.1)',
    '0 2px 4px rgba(0, 0, 0, 0.1)',
    '0 3px 6px rgba(0, 0, 0, 0.1)',
    '0 4px 8px rgba(0, 0, 0, 0.1)',
    '0 5px 10px rgba(0, 0, 0, 0.1)',
    '0 6px 12px rgba(0, 0, 0, 0.1)',
    '0 7px 14px rgba(0, 0, 0, 0.1)',
    '0 8px 16px rgba(0, 0, 0, 0.1)',
    '0 9px 18px rgba(0, 0, 0, 0.1)',
    '0 10px 20px rgba(0, 0, 0, 0.1)',
    '0 11px 22px rgba(0, 0, 0, 0.1)',
    '0 12px 24px rgba(0, 0, 0, 0.1)',
    '0 13px 26px rgba(0, 0, 0, 0.1)',
    '0 14px 28px rgba(0, 0, 0, 0.1)',
    '0 15px 30px rgba(0, 0, 0, 0.1)',
    '0 16px 32px rgba(0, 0, 0, 0.1)',
    '0 17px 34px rgba(0, 0, 0, 0.1)',
    '0 18px 36px rgba(0, 0, 0, 0.1)',
    '0 19px 38px rgba(0, 0, 0, 0.1)',
    '0 20px 40px rgba(0, 0, 0, 0.1)',
    '0 21px 42px rgba(0, 0, 0, 0.1)',
    '0 22px 44px rgba(0, 0, 0, 0.1)',
    '0 23px 46px rgba(0, 0, 0, 0.1)',
    '0 24px 48px rgba(0, 0, 0, 0.1)',
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          textTransform: 'none',
          fontWeight: 600,
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
          transition: 'all 0.2s ease',
          '&:hover': {
            transform: 'translateY(-1px)',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.15)',
          },
        },
        contained: {
          background: '#000000',
          color: '#ffffff',
          '&:hover': {
            background: '#333333',
          },
        },
        outlined: {
          borderColor: '#000000',
          color: '#000000',
          '&:hover': {
            borderColor: '#333333',
            background: 'rgba(0, 0, 0, 0.05)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          background: '#ffffff',
          border: '1px solid #e0e0e0',
          borderRadius: 8,
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          transition: 'all 0.2s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 4px 16px rgba(0, 0, 0, 0.15)',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 4,
            '& fieldset': {
              borderColor: '#e0e0e0',
            },
            '&:hover fieldset': {
              borderColor: '#000000',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#000000',
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          fontWeight: 500,
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: '#ffffff',
          borderBottom: '1px solid #e0e0e0',
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          background: '#ffffff',
          borderRight: '1px solid #e0e0e0',
          boxShadow: '2px 0 8px rgba(0, 0, 0, 0.1)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          background: '#ffffff',
          border: '1px solid #e0e0e0',
        },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          background: '#f5f5f5',
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:hover': {
            background: '#f9f9f9',
          },
        },
      },
    },
  },
});

export default theme;