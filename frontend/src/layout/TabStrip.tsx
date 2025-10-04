import React from 'react';
import { Tabs, Tab, Paper } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Dashboard as DashboardIcon,
  EventSeat as SeatingIcon,
  Assessment as EvaluationIcon,
  School as SchoolIcon,
  LocalHospital as ProtocolIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';

const TabStrip: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();

  const tabs = [
    { label: t('nav.dashboard'), value: '/dashboard', icon: <DashboardIcon /> },
    { label: t('nav.seatingPlan'), value: '/seating-plan', icon: <SeatingIcon /> },
    { label: t('nav.evaluations'), value: '/evaluations', icon: <EvaluationIcon /> },
    { label: t('nav.schoolLife'), value: '/school-life', icon: <SchoolIcon /> },
    { label: t('nav.protocols'), value: '/protocols', icon: <ProtocolIcon /> },
    { label: t('nav.settings'), value: '/settings', icon: <SettingsIcon /> },
  ];

  const currentTab = tabs.find((tab) => location.pathname.startsWith(tab.value))?.value || '/dashboard';

  const handleChange = (_event: React.SyntheticEvent, newValue: string) => {
    navigate(newValue);
  };

  return (
    <Paper square elevation={1}>
      <Tabs
        value={currentTab}
        onChange={handleChange}
        variant="scrollable"
        scrollButtons="auto"
        sx={{
          borderBottom: 1,
          borderColor: 'divider',
        }}
      >
        {tabs.map((tab) => (
          <Tab
            key={tab.value}
            label={tab.label}
            value={tab.value}
            icon={tab.icon}
            iconPosition="start"
          />
        ))}
      </Tabs>
    </Paper>
  );
};

export default TabStrip;
