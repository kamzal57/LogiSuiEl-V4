import { Box, Container } from '@mui/material';
import { Outlet } from 'react-router-dom';
import TopBar from './TopBar';
import TabStrip from './TabStrip';
import BottomBar from './BottomBar';

const MainShell = () => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <TopBar />
      <TabStrip />
      <Box component="main" sx={{ flexGrow: 1, bgcolor: 'background.default', py: 3 }}>
        <Container maxWidth="xl">
          <Outlet />
        </Container>
      </Box>
      <BottomBar />
    </Box>
  );
};

export default MainShell;
