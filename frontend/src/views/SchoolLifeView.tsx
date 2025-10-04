import React from 'react';
import { Box, Typography, Tabs, Tab, Paper } from '@mui/material';
import { useTranslation } from 'react-i18next';

export const SchoolLifeView: React.FC = () => {
  const { t } = useTranslation();
  const [currentTab, setCurrentTab] = React.useState(0);

  const tabs = [
    t('schoolLife.absences'),
    t('schoolLife.lates'),
    t('schoolLife.punishments'),
    t('schoolLife.exclusions'),
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('navigation.schoolLife')}
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
            <Typography>Absences tracking interface</Typography>
          )}
          {currentTab === 1 && (
            <Typography>Tardiness tracking interface</Typography>
          )}
          {currentTab === 2 && (
            <Typography>Punishments management interface</Typography>
          )}
          {currentTab === 3 && (
            <Typography>Exclusions management interface</Typography>
          )}
        </Box>
      </Paper>
    </Box>
  );
};
