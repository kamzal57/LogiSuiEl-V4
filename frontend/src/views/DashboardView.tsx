import React from 'react';
import { Paper, Typography, Box, Switch, FormControlLabel, Grid } from '@mui/material';
import { useTranslation } from 'react-i18next';

export const DashboardView: React.FC = () => {
  const { t } = useTranslation();
  const [modeClass, setModeClass] = React.useState(false);

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">{t('navigation.dashboard')}</Typography>
        <FormControlLabel
          control={
            <Switch
              checked={modeClass}
              onChange={(e) => setModeClass(e.target.checked)}
              color="primary"
            />
          }
          label={t('dashboard.modeClass')}
        />
      </Box>

      <Grid container spacing={3}>
        {/* Schedule - 40% */}
        <Grid size={{ xs: 12, md: 5 }}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              {t('dashboard.schedule')}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Weekly schedule will be displayed here
            </Typography>
          </Paper>
        </Grid>

        {/* Reminders - 30% */}
        <Grid size={{ xs: 12, md: 3 }}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              {t('dashboard.reminders')}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Notes, agenda, meetings
            </Typography>
          </Paper>
        </Grid>

        {/* Incidents - 30% */}
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              {t('dashboard.incidents')}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Detentions, calls, parent meetings, reminders
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};
