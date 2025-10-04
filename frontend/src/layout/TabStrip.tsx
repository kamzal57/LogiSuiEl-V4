import { Tabs, Tab, Box } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  EventSeat as SeatIcon,
  Assessment as AssessmentIcon,
  School as SchoolIcon,
  Description as DescriptionIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';

const TabStrip = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const tabs = [
    { label: 'Tableau de bord', value: '/dashboard', icon: <DashboardIcon /> },
    { label: 'Élèves', value: '/students', icon: <PeopleIcon /> },
    { label: 'Plan de classe', value: '/seating', icon: <SeatIcon /> },
    { label: 'Évaluations', value: '/evaluations', icon: <AssessmentIcon /> },
    { label: 'Vie scolaire', value: '/school-life', icon: <SchoolIcon /> },
    { label: 'Protocoles', value: '/protocols', icon: <DescriptionIcon /> },
    { label: 'Configuration', value: '/settings', icon: <SettingsIcon /> },
  ];

  const currentTab = tabs.find(tab => location.pathname.startsWith(tab.value))?.value || '/dashboard';

  const handleChange = (_event: React.SyntheticEvent, newValue: string) => {
    navigate(newValue);
  };

  return (
    <Box sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: 'background.paper' }}>
      <Tabs
        value={currentTab}
        onChange={handleChange}
        variant="scrollable"
        scrollButtons="auto"
        aria-label="main navigation tabs"
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
    </Box>
  );
};

export default TabStrip;
