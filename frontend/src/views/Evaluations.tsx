import { Typography, Box, Tabs, Tab } from '@mui/material';
import { useState } from 'react';

const Evaluations = () => {
  const [currentTab, setCurrentTab] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Évaluations
      </Typography>

      <Tabs value={currentTab} onChange={handleTabChange} sx={{ mb: 3 }}>
        <Tab label="Compétences" />
        <Tab label="Notes" />
        <Tab label="Bilans" />
      </Tabs>

      {currentTab === 0 && (
        <Typography variant="body1" color="text.secondary">
          Évaluation des compétences par élève.
        </Typography>
      )}
      {currentTab === 1 && (
        <Typography variant="body1" color="text.secondary">
          Gestion des notes.
        </Typography>
      )}
      {currentTab === 2 && (
        <Typography variant="body1" color="text.secondary">
          Bilans périodiques.
        </Typography>
      )}
    </Box>
  );
};

export default Evaluations;
