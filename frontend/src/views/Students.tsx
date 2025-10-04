import { Typography, Box } from '@mui/material';

const Students = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Gestion des Élèves
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Liste des élèves avec possibilité d'import CSV.
      </Typography>
    </Box>
  );
};

export default Students;
