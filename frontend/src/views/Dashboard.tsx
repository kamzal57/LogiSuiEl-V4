import React from 'react';
import { Box, Grid, Paper, Typography, Card, CardContent, CardHeader } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import api from '../api/client';

interface DashboardData {
  timetable_events: any[];
  reminders: any[];
  incidents: any[];
  upcoming_appointments: any[];
}

const Dashboard: React.FC = () => {
  const { data, isLoading, error } = useQuery<DashboardData>({
    queryKey: ['dashboard'],
    queryFn: async () => {
      const response = await api.get('/dashboard/');
      return response.data;
    },
  });

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography color="error">Error loading dashboard</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Timetable - 40% */}
        <Grid item xs={12} md={5}>
          <Card>
            <CardHeader title="This Week's Schedule" />
            <CardContent>
              {data?.timetable_events && data.timetable_events.length > 0 ? (
                data.timetable_events.map((event: any) => (
                  <Paper key={event.id} sx={{ p: 2, mb: 1 }} elevation={1}>
                    <Typography variant="subtitle2">{event.title}</Typography>
                    <Typography variant="caption" color="textSecondary">
                      {new Date(event.start_time).toLocaleString()} - {event.class_name}
                    </Typography>
                  </Paper>
                ))
              ) : (
                <Typography color="textSecondary">No events scheduled</Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Reminders - 30% */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader title="Reminders & Notes" />
            <CardContent>
              {data?.reminders && data.reminders.length > 0 ? (
                data.reminders.map((reminder: any) => (
                  <Paper key={reminder.id} sx={{ p: 2, mb: 1 }} elevation={1}>
                    <Typography variant="subtitle2">{reminder.title}</Typography>
                    <Typography variant="caption" color="textSecondary">
                      {reminder.type} - Priority: {reminder.priority}
                    </Typography>
                  </Paper>
                ))
              ) : (
                <Typography color="textSecondary">No reminders</Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Incidents & Appointments - 30% */}
        <Grid item xs={12} md={3}>
          <Card sx={{ mb: 2 }}>
            <CardHeader title="Upcoming Appointments" />
            <CardContent>
              {data?.upcoming_appointments && data.upcoming_appointments.length > 0 ? (
                data.upcoming_appointments.map((appt: any) => (
                  <Paper key={appt.id} sx={{ p: 1, mb: 1 }} elevation={1}>
                    <Typography variant="caption">{appt.title}</Typography>
                  </Paper>
                ))
              ) : (
                <Typography variant="caption" color="textSecondary">
                  No appointments
                </Typography>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader title="Recent Incidents" />
            <CardContent>
              {data?.incidents && data.incidents.length > 0 ? (
                <Typography variant="caption">
                  {data.incidents.length} incidents recorded
                </Typography>
              ) : (
                <Typography variant="caption" color="textSecondary">
                  No incidents
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
