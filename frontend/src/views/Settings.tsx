import React, { useState } from 'react';
import { Box, Typography, Tabs, Tab, Paper, TextField, Button } from '@mui/material';
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

const Settings: React.FC = () => {
  const { t } = useTranslation();
  const [currentTab, setCurrentTab] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('nav.settings')}
      </Typography>

      <Paper sx={{ mt: 3 }}>
        <Tabs value={currentTab} onChange={handleTabChange}>
          <Tab label={t('settings.personal')} />
          <Tab label={t('settings.school')} />
          <Tab label={t('settings.timetable')} />
          <Tab label={t('settings.periods')} />
          <Tab label={t('settings.appearance')} />
        </Tabs>

        <TabPanel value={currentTab} index={0}>
          <Typography variant="h6" gutterBottom>
            {t('settings.personal')}
          </Typography>
          <Box component="form" sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="Full Name"
              margin="normal"
              placeholder="Enter your full name"
            />
            <TextField
              fullWidth
              label="Email"
              margin="normal"
              type="email"
              placeholder="Enter your email"
            />
            <Button variant="contained" sx={{ mt: 2 }}>
              {t('app.save')}
            </Button>
          </Box>
        </TabPanel>

        <TabPanel value={currentTab} index={1}>
          <Typography variant="h6" gutterBottom>
            {t('settings.school')}
          </Typography>
          <Box component="form" sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="School Name"
              margin="normal"
              placeholder="Enter school name"
            />
            <TextField
              fullWidth
              label="School Address"
              margin="normal"
              multiline
              rows={3}
              placeholder="Enter school address"
            />
            <Typography variant="subtitle2" sx={{ mt: 3, mb: 2 }}>
              Import Data
            </Typography>
            <Button variant="outlined" component="label" sx={{ mr: 2 }}>
              Import Students CSV
              <input type="file" hidden accept=".csv" />
            </Button>
            <Button variant="outlined" component="label">
              Import Competences CSV
              <input type="file" hidden accept=".csv" />
            </Button>
            <Button variant="contained" sx={{ mt: 3, display: 'block' }}>
              {t('app.save')}
            </Button>
          </Box>
        </TabPanel>

        <TabPanel value={currentTab} index={2}>
          <Typography variant="h6" gutterBottom>
            {t('settings.timetable')}
          </Typography>
          <Box component="form" sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="ICS URL"
              margin="normal"
              placeholder="Enter ICS calendar URL"
              helperText="URL to download your timetable in ICS format"
            />
            <Button variant="contained" sx={{ mt: 2 }}>
              Import Timetable
            </Button>
          </Box>
        </TabPanel>

        <TabPanel value={currentTab} index={3}>
          <Typography variant="h6" gutterBottom>
            {t('settings.periods')}
          </Typography>
          <Typography color="text.secondary">
            Configure school year, trimesters, vacations, and holidays.
          </Typography>
        </TabPanel>

        <TabPanel value={currentTab} index={4}>
          <Typography variant="h6" gutterBottom>
            {t('settings.appearance')}
          </Typography>
          <Typography color="text.secondary">
            Customize the appearance and theme of the application.
          </Typography>
        </TabPanel>
      </Paper>
    </Box>
  );
};

export default Settings;
