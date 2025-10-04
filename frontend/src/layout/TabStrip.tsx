import React from 'react';
import { Tabs, Tab, Box } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

export const TabStrip: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();

  const tabs = [
    { label: t('navigation.dashboard'), path: '/dashboard' },
    { label: t('navigation.seatingPlan'), path: '/seating-plan' },
    { label: t('navigation.evaluations'), path: '/evaluations' },
    { label: t('navigation.schoolLife'), path: '/school-life' },
    { label: t('navigation.protocols'), path: '/protocols' },
    { label: t('navigation.settings'), path: '/settings' },
  ];

  const currentTab = tabs.findIndex(tab => location.pathname.startsWith(tab.path));

  return (
    <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
      <Tabs 
        value={currentTab !== -1 ? currentTab : 0} 
        onChange={(_, newValue) => navigate(tabs[newValue].path)}
        variant="scrollable"
        scrollButtons="auto"
      >
        {tabs.map((tab, index) => (
          <Tab key={index} label={tab.label} />
        ))}
      </Tabs>
    </Box>
  );
};
