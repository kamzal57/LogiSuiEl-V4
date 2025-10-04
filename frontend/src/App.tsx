import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider, useAuth } from './context/AuthProvider';
import { theme } from './theme';
import './locales/i18n';

import { MainShell } from './layout/MainShell';
import { LoginView } from './views/LoginView';
import { DashboardView } from './views/DashboardView';
import { SeatingPlanView } from './views/SeatingPlanView';
import { EvaluationsView } from './views/EvaluationsView';
import { SchoolLifeView } from './views/SchoolLifeView';
import { ProtocolsView } from './views/ProtocolsView';
import { SettingsView } from './views/SettingsView';

const queryClient = new QueryClient();

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AuthProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/login" element={<LoginView />} />
              <Route
                path="/*"
                element={
                  <ProtectedRoute>
                    <MainShell>
                      <Routes>
                        <Route path="/dashboard" element={<DashboardView />} />
                        <Route path="/seating-plan" element={<SeatingPlanView />} />
                        <Route path="/evaluations" element={<EvaluationsView />} />
                        <Route path="/school-life" element={<SchoolLifeView />} />
                        <Route path="/protocols" element={<ProtocolsView />} />
                        <Route path="/settings" element={<SettingsView />} />
                        <Route path="/" element={<Navigate to="/dashboard" />} />
                      </Routes>
                    </MainShell>
                  </ProtectedRoute>
                }
              />
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
