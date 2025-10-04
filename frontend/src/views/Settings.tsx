import { Typography, Box, Paper, Divider } from '@mui/material';

const Settings = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Configuration
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Informations personnelles
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Configuration du compte utilisateur.
        </Typography>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Établissement
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Informations sur l'établissement scolaire.
        </Typography>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Import de données
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Import CSV (élèves, compétences) et ICS (emploi du temps).
        </Typography>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Emploi du temps
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Configuration des heures, semaines A/B.
        </Typography>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Périodes et vacances
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Configuration des trimestres, année scolaire, vacances, jours fériés.
        </Typography>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Apparence
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Style et thème de l'application.
        </Typography>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Sécurité
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Gestion des identifiants et mots de passe.
        </Typography>
      </Paper>
    </Box>
  );
};

export default Settings;
