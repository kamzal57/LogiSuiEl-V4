import React from 'react';
import { Box } from '@mui/material';
import { TopBar } from './TopBar';
import { TabStrip } from './TabStrip';
import { BottomBar } from './BottomBar';

interface MainShellProps {
  children: React.ReactNode;
}

export const MainShell: React.FC<MainShellProps> = ({ children }) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <TopBar />
      <TabStrip />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        {children}
      </Box>
      <BottomBar />
    </Box>
  );
};
