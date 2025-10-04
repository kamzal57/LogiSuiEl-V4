import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authApi, User, UserPreferences, LoginCredentials } from '../api/auth';

interface AuthContextType {
  user: User | null;
  preferences: UserPreferences | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  updatePreferences: (prefs: Partial<UserPreferences>) => Promise<void>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [preferences, setPreferences] = useState<UserPreferences | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const currentUser = await authApi.getCurrentUser();
          setUser(currentUser);
          const userPrefs = await authApi.getPreferences();
          setPreferences(userPrefs);
        } catch (error) {
          console.error('Failed to fetch user:', error);
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    const authResponse = await authApi.login(credentials);
    localStorage.setItem('access_token', authResponse.access_token);
    localStorage.setItem('refresh_token', authResponse.refresh_token);
    
    const currentUser = await authApi.getCurrentUser();
    setUser(currentUser);
    const userPrefs = await authApi.getPreferences();
    setPreferences(userPrefs);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    setPreferences(null);
  };

  const updatePreferences = async (prefs: Partial<UserPreferences>) => {
    const updated = await authApi.updatePreferences(prefs);
    setPreferences(updated);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        preferences,
        login,
        logout,
        updatePreferences,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
