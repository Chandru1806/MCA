import { User } from './User';

export interface AuthResponse {
  success: boolean;
  message: string;
  data: {
    access_token: string;
    refresh_token: string;
    token_type: string;
    expires_in: number;
    user: User;
  };
}

export interface AuthError {
  message: string;
  errors?: Record<string, string[]>;
}
