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

const SchoolLife: React.FC = () => {
  const { t } = useTranslation();
  const [currentTab, setCurrentTab] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('nav.schoolLife')}
      </Typography>

      <Paper sx={{ mt: 3 }}>
        <Tabs value={currentTab} onChange={handleTabChange}>
          <Tab label={t('schoolLife.absences')} />
          <Tab label={t('schoolLife.lates')} />
          <Tab label={t('schoolLife.punishments')} />
          <Tab label={t('schoolLife.exclusions')} />
          <Tab label={t('schoolLife.notes')} />
        </Tabs>

        <TabPanel value={currentTab} index={0}>
          <Typography variant="h6" gutterBottom>
            {t('schoolLife.absences')}
          </Typography>
          <Typography color="text.secondary">
            Track and manage student absences.
          </Typography>
        </TabPanel>

        <TabPanel value={currentTab} index={1}>
          <Typography variant="h6" gutterBottom>
            {t('schoolLife.lates')}
          </Typography>
          <Typography color="text.secondary">
            Record tardiness and late arrivals.
          </Typography>
        </TabPanel>

        <TabPanel value={currentTab} index={2}>
          <Typography variant="h6" gutterBottom>
            {t('schoolLife.punishments')}
          </Typography>
          <Typography color="text.secondary">
            Manage punishments and disciplinary actions.
          </Typography>
        </TabPanel>

        <TabPanel value={currentTab} index={3}>
          <Typography variant="h6" gutterBottom>
            {t('schoolLife.exclusions')}
          </Typography>
          <Typography color="text.secondary">
            Track exclusions and suspensions.
          </Typography>
        </TabPanel>

        <TabPanel value={currentTab} index={4}>
          <Typography variant="h6" gutterBottom>
            {t('schoolLife.notes')}
          </Typography>
          <Typography color="text.secondary">
            Personal notes and observations about students.
          </Typography>
        </TabPanel>
      </Paper>
    </Box>
  );
};

export default SchoolLife;
