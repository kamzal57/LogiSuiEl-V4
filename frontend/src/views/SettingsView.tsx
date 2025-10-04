import React from 'react';
import { Box, Typography, Paper, Tabs, Tab } from '@mui/material';
import { useTranslation } from 'react-i18next';

export const SettingsView: React.FC = () => {
  const { t } = useTranslation();
  const [currentTab, setCurrentTab] = React.useState(0);

  const tabs = [
    'Personal Info',
    'School Info',
    'Import/Export',
    'Schedule Config',
    'Periods',
    'Appearance',
    'Security',
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('navigation.settings')}
      </Typography>

      <Paper sx={{ mt: 2 }}>
        <Tabs
          value={currentTab}
          onChange={(_, newValue) => setCurrentTab(newValue)}
          sx={{ borderBottom: 1, borderColor: 'divider' }}
          variant="scrollable"
          scrollButtons="auto"
        >
          {tabs.map((tab, index) => (
            <Tab key={index} label={tab} />
          ))}
        </Tabs>

        <Box sx={{ p: 3 }}>
          <Typography variant="body1">
            {tabs[currentTab]} configuration interface
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            Configuration options for {tabs[currentTab].toLowerCase()}
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
};
