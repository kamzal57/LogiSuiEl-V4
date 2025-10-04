import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Button, List, ListItem, ListItemText, Divider } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import { protocolsApi } from '../api';
import type { Protocol } from '../api/types';

const Protocols: React.FC = () => {
  const { t } = useTranslation();
  const [protocols, setProtocols] = useState<Protocol[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProtocols = async () => {
      try {
        const data = await protocolsApi.getAll();
        setProtocols(data);
      } catch (error) {
        console.error('Failed to fetch protocols:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProtocols();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography>{t('app.loading')}</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          {t('nav.protocols')}
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            // This would open a dialog for adding a protocol
            console.log('Add protocol');
          }}
        >
          {t('protocols.addProtocol')}
        </Button>
      </Box>

      <Paper sx={{ p: 3 }}>
        <Typography variant="body1" color="text.secondary" gutterBottom>
          PAI (Projet d'Accueil Individualisé) and other protocols for students requiring special attention.
        </Typography>

        {protocols.length > 0 ? (
          <List>
            {protocols.map((protocol, index) => (
              <React.Fragment key={protocol.id}>
                <ListItem>
                  <ListItemText
                    primary={protocol.protocol_type}
                    secondary={
                      <>
                        <Typography variant="body2" component="span">
                          {protocol.description}
                        </Typography>
                        <br />
                        <Typography variant="caption" color="text.secondary">
                          From: {new Date(protocol.start_date).toLocaleDateString()}
                          {protocol.end_date && ` - To: ${new Date(protocol.end_date).toLocaleDateString()}`}
                        </Typography>
                      </>
                    }
                  />
                </ListItem>
                {index < protocols.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        ) : (
          <Typography color="text.secondary" align="center" sx={{ mt: 4 }}>
            No protocols defined yet.
          </Typography>
        )}
      </Paper>
    </Box>
  );
};

export default Protocols;
