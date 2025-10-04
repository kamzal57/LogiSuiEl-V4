import React from 'react';
import { Box, Typography, Tabs, Tab, Paper } from '@mui/material';
import { useTranslation } from 'react-i18next';

export const EvaluationsView: React.FC = () => {
  const { t } = useTranslation();
  const [currentTab, setCurrentTab] = React.useState(0);

  const tabs = [
    t('evaluations.competences'),
    t('evaluations.notes'),
    t('evaluations.reports'),
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('navigation.evaluations')}
      </Typography>

      <Paper sx={{ mt: 2 }}>
        <Tabs
          value={currentTab}
          onChange={(_, newValue) => setCurrentTab(newValue)}
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          {tabs.map((tab, index) => (
            <Tab key={index} label={tab} />
          ))}
        </Tabs>

        <Box sx={{ p: 3 }}>
          {currentTab === 0 && (
            <Typography>Skills evaluation interface</Typography>
          )}
          {currentTab === 1 && (
            <Typography>Grades management interface</Typography>
          )}
          {currentTab === 2 && (
            <Typography>Reports generation interface</Typography>
          )}
        </Box>
      </Paper>
    </Box>
  );
};
