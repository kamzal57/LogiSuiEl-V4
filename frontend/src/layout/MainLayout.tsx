import React, { useState } from 'react';
import { Box } from '@mui/material';
import { Outlet } from 'react-router-dom';
import TopBar from './TopBar';
import TabStrip from './TabStrip';
import BottomBar from './BottomBar';

const MainLayout: React.FC = () => {
  const [classModeEnabled, setClassModeEnabled] = useState(false);

  const handleSave = () => {
    // This will be implemented when we add the save functionality
    console.log('Save triggered');
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <TopBar
        onSave={handleSave}
        classModeEnabled={classModeEnabled}
        onClassModeToggle={setClassModeEnabled}
      />
      <TabStrip />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          bgcolor: 'background.default',
          mb: 6, // space for bottom bar
        }}
      >
        <Outlet context={{ classModeEnabled }} />
      </Box>
      <BottomBar />
    </Box>
  );
};

export default MainLayout;
