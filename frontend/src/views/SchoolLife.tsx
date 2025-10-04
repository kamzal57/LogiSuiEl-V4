import { Typography, Box, Tabs, Tab } from '@mui/material';
import { useState } from 'react';

const SchoolLife = () => {
  const [currentTab, setCurrentTab] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Vie Scolaire
      </Typography>

      <Tabs value={currentTab} onChange={handleTabChange} sx={{ mb: 3 }}>
        <Tab label="Absences" />
        <Tab label="Retards" />
        <Tab label="Incidents" />
        <Tab label="Punitions" />
        <Tab label="Exclusions" />
      </Tabs>

      {currentTab === 0 && (
        <Typography variant="body1" color="text.secondary">
          Gestion des absences.
        </Typography>
      )}
      {currentTab === 1 && (
        <Typography variant="body1" color="text.secondary">
          Gestion des retards.
        </Typography>
      )}
      {currentTab === 2 && (
        <Typography variant="body1" color="text.secondary">
          Gestion des incidents comportementaux.
        </Typography>
      )}
      {currentTab === 3 && (
        <Typography variant="body1" color="text.secondary">
          Gestion des punitions.
        </Typography>
      )}
      {currentTab === 4 && (
        <Typography variant="body1" color="text.secondary">
          Gestion des exclusions.
        </Typography>
      )}
    </Box>
  );
};

export default SchoolLife;
