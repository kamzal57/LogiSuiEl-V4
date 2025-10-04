import React from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Box, Switch, FormControlLabel } from '@mui/material';
import { Save as SaveIcon, Logout as LogoutIcon, Language as LanguageIcon } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthProvider';

interface TopBarProps {
  onSave?: () => void;
  classModeEnabled: boolean;
  onClassModeToggle: (enabled: boolean) => void;
}

const TopBar: React.FC<TopBarProps> = ({ onSave, classModeEnabled, onClassModeToggle }) => {
  const { t, i18n } = useTranslation();
  const { user, logout } = useAuth();

  const toggleLanguage = () => {
    const newLang = i18n.language === 'fr' ? 'en' : 'fr';
    i18n.changeLanguage(newLang);
  };

  return (
    <AppBar position="static" sx={{ bgcolor: 'primary.main' }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          {t('app.title')}
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <FormControlLabel
            control={
              <Switch
                checked={classModeEnabled}
                onChange={(e) => onClassModeToggle(e.target.checked)}
                color="default"
              />
            }
            label={t('dashboard.classMode')}
          />

          {onSave && (
            <Button
              color="inherit"
              startIcon={<SaveIcon />}
              onClick={onSave}
            >
              {t('app.save')}
            </Button>
          )}

          <IconButton color="inherit" onClick={toggleLanguage}>
            <LanguageIcon />
          </IconButton>

          <Typography variant="body2" sx={{ mr: 1 }}>
            {user?.username}
          </Typography>

          <IconButton color="inherit" onClick={logout}>
            <LogoutIcon />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default TopBar;
