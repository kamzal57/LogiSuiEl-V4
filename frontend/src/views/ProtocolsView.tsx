import React from 'react';
import { Box, Typography, Paper, List, ListItem, ListItemText } from '@mui/material';
import { useTranslation } from 'react-i18next';

export const ProtocolsView: React.FC = () => {
  const { t } = useTranslation();

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('navigation.protocols')}
      </Typography>

      <Paper sx={{ p: 3, mt: 2 }}>
        <Typography variant="h6" gutterBottom>
          Student Protocols (PAI, etc.)
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          List of students with special protocols and required actions
        </Typography>

        <List sx={{ mt: 2 }}>
          <ListItem>
            <ListItemText
              primary="No protocols currently configured"
              secondary="Protocols will appear here once configured"
            />
          </ListItem>
        </List>
      </Paper>
    </Box>
  );
};
