import React, { useEffect, useState } from 'react';
import { Paper, Typography, Box, Card, CardContent, List, ListItem, ListItemText } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { dashboardApi } from '../api';
import type { DashboardData } from '../api/types';

const Dashboard: React.FC = () => {
  const { t } = useTranslation();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const dashboardData = await dashboardApi.getData();
        setData(dashboardData);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
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
      <Typography variant="h4" gutterBottom>
        {t('nav.dashboard')}
      </Typography>

      <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
        {/* Timetable - 40% */}
        <Box sx={{ flex: '1 1 40%', minWidth: '300px' }}>
          <Paper sx={{ p: 2, height: '500px', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              {t('dashboard.timetable')}
            </Typography>
            {data?.timetable && data.timetable.length > 0 ? (
              <List>
                {data.timetable.map((event) => (
                  <ListItem key={event.id}>
                    <Card sx={{ width: '100%', mb: 1 }}>
                      <CardContent>
                        <Typography variant="subtitle1" fontWeight="bold">
                          {event.title}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {new Date(event.start_time).toLocaleTimeString()} - {new Date(event.end_time).toLocaleTimeString()}
                        </Typography>
                        {event.location && (
                          <Typography variant="body2">{event.location}</Typography>
                        )}
                        {event.class_name && (
                          <Typography variant="body2">{event.class_name}</Typography>
                        )}
                      </CardContent>
                    </Card>
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography color="text.secondary">No events scheduled</Typography>
            )}
          </Paper>
        </Box>

        {/* Reminders - 30% */}
        <Box sx={{ flex: '1 1 25%', minWidth: '250px' }}>
          <Paper sx={{ p: 2, height: '500px', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              {t('dashboard.reminders')}
            </Typography>
            {data?.reminders && data.reminders.length > 0 ? (
              <List>
                {data.reminders.map((reminder) => (
                  <ListItem key={reminder.id}>
                    <ListItemText
                      primary={reminder.title}
                      secondary={reminder.description}
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography color="text.secondary">No reminders</Typography>
            )}
          </Paper>
        </Box>

        {/* Incidents - 30% */}
        <Box sx={{ flex: '1 1 25%', minWidth: '250px' }}>
          <Paper sx={{ p: 2, height: '500px', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              {t('dashboard.incidents')}
            </Typography>
            {data?.incidents && data.incidents.length > 0 ? (
              <List>
                {data.incidents.map((incident) => (
                  <ListItem key={incident.id}>
                    <Card sx={{ width: '100%', mb: 1 }}>
                      <CardContent>
                        <Typography variant="subtitle2" color="primary">
                          {incident.category}
                        </Typography>
                        <Typography variant="body2">
                          {incident.description}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(incident.date).toLocaleDateString()}
                        </Typography>
                      </CardContent>
                    </Card>
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography color="text.secondary">No incidents recorded</Typography>
            )}
          </Paper>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
