import { Typography, Box, Grid, Paper } from '@mui/material';

const Dashboard = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Tableau de bord
      </Typography>

      <Grid container spacing={3}>
        {/* Emploi du temps (40%) */}
        <Grid item xs={12} md={5}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              Emploi du temps de la semaine
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Les événements de la semaine s'afficheront ici.
            </Typography>
          </Paper>
        </Grid>

        {/* Pense-bête (30%) */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              Pense-bête & Agenda
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Notes personnelles, réunions et rappels.
            </Typography>
          </Paper>
        </Grid>

        {/* Rappels (30%) */}
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              Rappels
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Retenues, appels parents, rendez-vous.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
