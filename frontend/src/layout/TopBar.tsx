import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box, IconButton } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthProvider';
import SaveIcon from '@mui/icons-material/Save';
import LanguageIcon from '@mui/icons-material/Language';
import LogoutIcon from '@mui/icons-material/Logout';
import SchoolIcon from '@mui/icons-material/School';

export const TopBar: React.FC = () => {
  const { t, i18n } = useTranslation();
  const { user, logout } = useAuth();

  const toggleLanguage = () => {
    const newLang = i18n.language === 'fr' ? 'en' : 'fr';
    i18n.changeLanguage(newLang);
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <SchoolIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          {t('app.title')} - {user?.username}
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button color="inherit" startIcon={<SaveIcon />}>
            {t('actions.save')}
          </Button>
          <IconButton color="inherit" onClick={toggleLanguage}>
            <LanguageIcon />
          </IconButton>
          <Button color="inherit" startIcon={<LogoutIcon />} onClick={logout}>
            {t('auth.logout')}
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};
