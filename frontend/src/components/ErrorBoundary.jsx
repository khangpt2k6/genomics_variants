import React from 'react';
import { Box, Typography, Button, Card, CardContent } from '@mui/material';
import { ErrorOutline, Refresh } from '@mui/icons-material';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
    
    // Log error to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('ErrorBoundary caught an error:', error, errorInfo);
    }
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '50vh',
            p: 3,
          }}
        >
          <Card
            sx={{
              maxWidth: 500,
              background: '#ffffff',
              border: '1px solid #e0e0e0',
              borderRadius: 2,
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
              textAlign: 'center',
            }}
          >
            <CardContent sx={{ p: 4 }}>
              <ErrorOutline
                sx={{
                  fontSize: 64,
                  color: '#F44336',
                  mb: 2,
                  animation: 'pulse 2s infinite',
                }}
              />
              
              <Typography
                variant="h5"
                gutterBottom
                sx={{
                  color: '#000000',
                  fontWeight: 600,
                  mb: 2,
                }}
              >
                Oops! Something went wrong
              </Typography>
              
              <Typography
                variant="body1"
                color="text.secondary"
                sx={{ mb: 3, lineHeight: 1.6 }}
              >
                We encountered an unexpected error. Don't worry, our team has been notified
                and we're working to fix it.
              </Typography>
              
              {process.env.NODE_ENV === 'development' && this.state.error && (
                <Box
                  sx={{
                    mt: 3,
                    p: 2,
                    background: 'rgba(244, 67, 54, 0.1)',
                    borderRadius: 2,
                    border: '1px solid rgba(244, 67, 54, 0.2)',
                  }}
                >
                  <Typography
                    variant="body2"
                    sx={{
                      fontFamily: 'monospace',
                      fontSize: '0.8rem',
                      color: '#D32F2F',
                      textAlign: 'left',
                      wordBreak: 'break-word',
                    }}
                  >
                    {this.state.error.toString()}
                  </Typography>
                </Box>
              )}
              
              <Button
                variant="contained"
                startIcon={<Refresh />}
                onClick={this.handleRetry}
                sx={{
                  mt: 3,
                  background: '#000000',
                  color: '#ffffff',
                  borderRadius: 2,
                  px: 3,
                  py: 1.5,
                  '&:hover': {
                    background: '#333333',
                    transform: 'translateY(-1px)',
                    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
                  },
                  transition: 'all 0.3s ease',
                }}
              >
                Try Again
              </Button>
            </CardContent>
          </Card>
        </Box>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
