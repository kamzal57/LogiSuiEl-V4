import api from './client';

export interface User {
  id: number;
  username: string;
  email?: string;
  full_name?: string;
  role: string;
  is_active: boolean;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<TokenResponse> => {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await api.post<TokenResponse>('/auth/token', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  getPreferences: async () => {
    const response = await api.get('/auth/preferences');
    return response.data;
  },

  updatePreferences: async (preferences: any) => {
    const response = await api.put('/auth/preferences', preferences);
    return response.data;
  },
};
