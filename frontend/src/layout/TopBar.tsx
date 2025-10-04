import { AppBar, Toolbar, Typography, Button, Box, Switch, FormControlLabel } from '@mui/material';
import { Save as SaveIcon, Language as LanguageIcon, School as SchoolIcon } from '@mui/icons-material';
import { useAuth } from '../context/AuthProvider';

const TopBar = () => {
  const { user, preferences, updatePreferences, logout } = useAuth();

  const handleClassModeToggle = async (event: React.ChangeEvent<HTMLInputElement>) => {
    await updatePreferences({ class_mode: event.target.checked });
  };

  const handleLanguageToggle = async () => {
    const newLang = preferences?.language === 'fr' ? 'en' : 'fr';
    await updatePreferences({ language: newLang });
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <SchoolIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          LogiSuiEl
        </Typography>
        
        <FormControlLabel
          control={
            <Switch
              checked={preferences?.class_mode || false}
              onChange={handleClassModeToggle}
              color="default"
            />
          }
          label="Mode Classe"
          sx={{ mr: 2, color: 'white' }}
        />
        
        <Button color="inherit" startIcon={<SaveIcon />} sx={{ mr: 1 }}>
          Enregistrer
        </Button>
        
        <Button color="inherit" startIcon={<LanguageIcon />} onClick={handleLanguageToggle} sx={{ mr: 1 }}>
          {preferences?.language?.toUpperCase() || 'FR'}
        </Button>
        
        <Typography variant="body2" sx={{ mr: 2 }}>
          {user?.username} ({user?.role})
        </Typography>
        
        <Button color="inherit" onClick={logout}>
          Déconnexion
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default TopBar;
