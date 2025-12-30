import apiClient from '../utils/apiClient';
import { ForgotPasswordRequest } from '../models/ForgotPasswordRequest';
import { ResetPasswordRequest } from '../models/ResetPasswordRequest';
import { ForgotPasswordResponse } from '../models/ForgotPasswordResponse';

export const forgotPasswordService = {
  verifyEmail: async (data: ForgotPasswordRequest): Promise<ForgotPasswordResponse> => {
    const response = await apiClient.post<ForgotPasswordResponse>('/api/auth/verify-email', data);
    return response.data;
  },

  resetPassword: async (userId: string, data: ResetPasswordRequest): Promise<ForgotPasswordResponse> => {
    const response = await apiClient.put<ForgotPasswordResponse>(`/api/auth/profiles/${userId}`, data);
    return response.data;
  },
};
