export interface User {
  id: number;
  username: string;
  role: 'ADMIN' | 'TEACHER';
  full_name?: string;
  email?: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Student {
  id: number;
  first_name: string;
  last_name: string;
  class_name: string;
  student_id?: string;
  birth_date?: string;
  email?: string;
  phone?: string;
  notes?: string;
}

export interface Competence {
  id: number;
  code: string;
  name: string;
  description?: string;
  subject?: string;
}

export interface Evaluation {
  id: number;
  student_id: number;
  competence_id?: number;
  value: string;
  date: string;
  notes?: string;
  type: 'competence' | 'note';
}

export interface Behaviour {
  id: number;
  student_id: number;
  category: string;
  description: string;
  date: string;
  severity?: string;
}

export interface TimetableEvent {
  id: number;
  title: string;
  start_time: string;
  end_time: string;
  location?: string;
  class_name?: string;
  description?: string;
}

export interface Reminder {
  id: number;
  title: string;
  description?: string;
  due_date?: string;
  scope: 'PERSONAL' | 'CLASS' | 'SCHOOL';
  is_completed: boolean;
}

export interface SeatPosition {
  id: number;
  student_id: number;
  row: number;
  col: number;
}

export interface Protocol {
  id: number;
  student_id: number;
  protocol_type: string;
  description: string;
  actions: string;
  start_date: string;
  end_date?: string;
}

export interface AppConfig {
  school_name?: string;
  school_address?: string;
  periods?: any[];
  appearance?: any;
  class_mode_enabled?: boolean;
  widgets_enabled?: string[];
}

export interface DashboardData {
  timetable: TimetableEvent[];
  reminders: Reminder[];
  incidents: Behaviour[];
}
