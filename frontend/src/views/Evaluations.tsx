import React, { useState } from 'react';
import { Box, Typography, Tabs, Tab, Paper } from '@mui/material';
import { useTranslation } from 'react-i18next';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index }) => {
  return (
    <div hidden={value !== index} style={{ padding: '24px' }}>
      {value === index && <Box>{children}</Box>}
    </div>
  );
};

const Evaluations: React.FC = () => {
  const { t } = useTranslation();
  const [currentTab, setCurrentTab] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('nav.evaluations')}
      </Typography>

      <Paper sx={{ mt: 3 }}>
        <Tabs value={currentTab} onChange={handleTabChange}>
          <Tab label={t('evaluations.competences')} />
          <Tab label={t('evaluations.grades')} />
          <Tab label={t('evaluations.reports')} />
        </Tabs>

        <TabPanel value={currentTab} index={0}>
          <Typography variant="h6" gutterBottom>
            {t('evaluations.competences')}
          </Typography>
          <Typography color="text.secondary">
            Competence-based evaluations interface. Import competences from CSV in Settings.
          </Typography>
        </TabPanel>

        <TabPanel value={currentTab} index={1}>
          <Typography variant="h6" gutterBottom>
            {t('evaluations.grades')}
          </Typography>
          <Typography color="text.secondary">
            Traditional grades interface. Add evaluations for students here.
          </Typography>
        </TabPanel>

        <TabPanel value={currentTab} index={2}>
          <Typography variant="h6" gutterBottom>
            {t('evaluations.reports')}
          </Typography>
          <Typography color="text.secondary">
            Generate and view evaluation reports for students and classes.
          </Typography>
        </TabPanel>
      </Paper>
    </Box>
  );
};

export default Evaluations;
