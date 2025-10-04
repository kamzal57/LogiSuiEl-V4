import apiClient from './client';
import type {
  LoginRequest,
  LoginResponse,
  User,
  Student,
  Competence,
  Evaluation,
  Behaviour,
  TimetableEvent,
  Reminder,
  SeatPosition,
  Protocol,
  AppConfig,
  DashboardData,
} from './types';

// Auth API
export const authApi = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await apiClient.post('/auth/token', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  getProfile: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  refresh: async (refreshToken: string): Promise<LoginResponse> => {
    const response = await apiClient.post('/auth/refresh', { refresh_token: refreshToken });
    return response.data;
  },
};

// Students API
export const studentsApi = {
  getAll: async (): Promise<Student[]> => {
    const response = await apiClient.get('/students');
    return response.data;
  },

  getById: async (id: number): Promise<Student> => {
    const response = await apiClient.get(`/students/${id}`);
    return response.data;
  },

  create: async (student: Partial<Student>): Promise<Student> => {
    const response = await apiClient.post('/students', student);
    return response.data;
  },

  update: async (id: number, student: Partial<Student>): Promise<Student> => {
    const response = await apiClient.put(`/students/${id}`, student);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/students/${id}`);
  },

  importCSV: async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post('/students/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  addBehaviour: async (studentId: number, behaviour: Partial<Behaviour>): Promise<Behaviour> => {
    const response = await apiClient.post(`/students/${studentId}/behaviours`, behaviour);
    return response.data;
  },

  getBehaviours: async (studentId: number): Promise<Behaviour[]> => {
    const response = await apiClient.get(`/students/${studentId}/behaviours`);
    return response.data;
  },

  addEvaluation: async (studentId: number, evaluation: Partial<Evaluation>): Promise<Evaluation> => {
    const response = await apiClient.post(`/students/${studentId}/evaluations`, evaluation);
    return response.data;
  },

  getEvaluations: async (studentId: number): Promise<Evaluation[]> => {
    const response = await apiClient.get(`/students/${studentId}/evaluations`);
    return response.data;
  },
};

// Competences API
export const competencesApi = {
  getAll: async (): Promise<Competence[]> => {
    const response = await apiClient.get('/competences');
    return response.data;
  },

  importCSV: async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post('/competences/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
};

// Dashboard API
export const dashboardApi = {
  getData: async (): Promise<DashboardData> => {
    const response = await apiClient.get('/dashboard');
    return response.data;
  },
};

// Schedule API
export const scheduleApi = {
  getEvents: async (): Promise<TimetableEvent[]> => {
    const response = await apiClient.get('/schedule');
    return response.data;
  },

  importICS: async (url: string): Promise<any> => {
    const response = await apiClient.post('/schedule/import-ics', { url });
    return response.data;
  },
};

// Reminders API
export const remindersApi = {
  getAll: async (): Promise<Reminder[]> => {
    const response = await apiClient.get('/reminders');
    return response.data;
  },

  create: async (reminder: Partial<Reminder>): Promise<Reminder> => {
    const response = await apiClient.post('/reminders', reminder);
    return response.data;
  },

  update: async (id: number, reminder: Partial<Reminder>): Promise<Reminder> => {
    const response = await apiClient.put(`/reminders/${id}`, reminder);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/reminders/${id}`);
  },
};

// Seating Plan API
export const seatingApi = {
  getSeating: async (): Promise<SeatPosition[]> => {
    const response = await apiClient.get('/seating-plan');
    return response.data;
  },

  updateSeating: async (seats: SeatPosition[]): Promise<SeatPosition[]> => {
    const response = await apiClient.post('/seating-plan', { seats });
    return response.data;
  },
};

// Protocols API
export const protocolsApi = {
  getAll: async (): Promise<Protocol[]> => {
    const response = await apiClient.get('/protocols');
    return response.data;
  },

  create: async (protocol: Partial<Protocol>): Promise<Protocol> => {
    const response = await apiClient.post('/protocols', protocol);
    return response.data;
  },

  update: async (id: number, protocol: Partial<Protocol>): Promise<Protocol> => {
    const response = await apiClient.put(`/protocols/${id}`, protocol);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/protocols/${id}`);
  },
};

// Config API
export const configApi = {
  getConfig: async (): Promise<AppConfig> => {
    const response = await apiClient.get('/config');
    return response.data;
  },

  updateConfig: async (config: Partial<AppConfig>): Promise<AppConfig> => {
    const response = await apiClient.put('/config', config);
    return response.data;
  },
};

// Reports API
export const reportsApi = {
  exportStudents: async (): Promise<Blob> => {
    const response = await apiClient.get('/reports/students', { responseType: 'blob' });
    return response.data;
  },

  exportEvaluations: async (): Promise<Blob> => {
    const response = await apiClient.get('/reports/evaluations', { responseType: 'blob' });
    return response.data;
  },
};
