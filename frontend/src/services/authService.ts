import apiClient from '../utils/apiClient';
import { AuthResponse } from '../models/AuthResponse';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupCredentials {
  email: string;
  password: string;
  confirmPassword: string;
}

export const authService = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/auth/login', credentials);
    return response.data;
  },

  signup: async (credentials: SignupCredentials): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/auth/signup', credentials);
    return response.data;
  },
};
