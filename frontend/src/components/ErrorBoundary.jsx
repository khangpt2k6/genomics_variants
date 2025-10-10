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
              background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 187, 208, 0.1) 50%, rgba(156, 39, 176, 0.1) 100%)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(233, 30, 99, 0.1)',
              borderRadius: 3,
              boxShadow: '0 8px 32px rgba(233, 30, 99, 0.15)',
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
                  background: 'linear-gradient(135deg, #F44336, #D32F2F)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
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
                  background: 'linear-gradient(135deg, #E91E63, #9C27B0)',
                  borderRadius: 2,
                  px: 3,
                  py: 1.5,
                  '&:hover': {
                    background: 'linear-gradient(135deg, #C2185B, #7B1FA2)',
                    transform: 'translateY(-2px)',
                    boxShadow: '0 8px 24px rgba(233, 30, 99, 0.3)',
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
