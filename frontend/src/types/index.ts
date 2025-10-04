export type Role = 'ADMIN' | 'TEACHER';

export interface User {
  id: number;
  username: string;
  full_name?: string;
  email?: string;
  role: Role;
  is_active: boolean;
  preferences?: UserPreferences;
}

export interface UserPreferences {
  locale: string;
  mode_class_only: boolean;
  available_widgets: Record<string, boolean>;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface Student {
  id: number;
  first_name: string;
  last_name: string;
  class_name?: string;
  email?: string;
  birth_date?: string;
}

export interface TimetableEvent {
  id: number;
  title: string;
  start_time: string;
  end_time: string;
  location?: string;
  description?: string;
}

export interface Reminder {
  id: number;
  title: string;
  description?: string;
  due_date?: string;
  scope: string;
}

export interface Incident {
  id: number;
  student_id: number;
  category: string;
  description: string;
  date: string;
  is_positive: boolean;
}

export interface Protocol {
  id: number;
  student_id: number;
  protocol_type: string;
  title: string;
  description?: string;
  actions: string[];
}

export interface SeatingPosition {
  student_id: number;
  row: number;
  col: number;
}
