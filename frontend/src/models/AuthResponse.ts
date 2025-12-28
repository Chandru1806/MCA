import { User } from './User';

export interface AuthResponse {
  message: string;
  token: string;
  user: User;
}

export interface AuthError {
  message: string;
  errors?: Record<string, string[]>;
}
