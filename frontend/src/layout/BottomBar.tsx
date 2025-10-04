import React from 'react';
import { Typography, Paper } from '@mui/material';

const BottomBar: React.FC = () => {
  return (
    <Paper
      square
      elevation={3}
      sx={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        p: 1,
        textAlign: 'center',
        bgcolor: 'background.paper',
      }}
    >
      <Typography variant="caption" color="text.secondary">
        LogiSuiEl V4 - © 2025
      </Typography>
    </Paper>
  );
};

export default BottomBar;
