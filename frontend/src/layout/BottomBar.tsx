import { Box, Typography, Link } from '@mui/material';

const BottomBar = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 2,
        px: 3,
        mt: 'auto',
        bgcolor: 'background.paper',
        borderTop: 1,
        borderColor: 'divider',
      }}
    >
      <Typography variant="body2" color="text.secondary" align="center">
        © 2024 LogiSuiEl v4.0.0 - Gestion scolaire |{' '}
        <Link color="inherit" href="https://github.com/kamzal57/LogiSuiEl-V4">
          GitHub
        </Link>
      </Typography>
    </Box>
  );
};

export default BottomBar;
