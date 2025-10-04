import { Typography, Box } from '@mui/material';

const Protocols = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Protocoles (PAI, PAP, etc.)
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Liste des élèves concernés par des protocoles spéciaux et actions à entreprendre.
      </Typography>
    </Box>
  );
};

export default Protocols;
