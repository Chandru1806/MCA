import { forgotPasswordService } from '../services/forgotPasswordService';
import { ForgotPasswordRequest } from '../models/ForgotPasswordRequest';
import { ResetPasswordRequest } from '../models/ResetPasswordRequest';

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

export const forgotPasswordController = {
  validateEmail: (email: string): string | null => {
    if (!email.trim()) return 'Email is required';
    if (!EMAIL_REGEX.test(email)) return 'Invalid email format';
    return null;
  },

  validatePassword: (password: string, confirmPassword: string): { password?: string; confirmPassword?: string } => {
    const errors: { password?: string; confirmPassword?: string } = {};

    if (!password.trim()) {
      errors.password = 'Password is required';
    } else if (!PASSWORD_REGEX.test(password)) {
      errors.password = 'Password must be at least 8 characters with 1 uppercase, 1 lowercase, and 1 number';
    }

    if (!confirmPassword.trim()) {
      errors.confirmPassword = 'Confirm password is required';
    } else if (password !== confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }

    return errors;
  },

  handleForgotPassword: async (data: ForgotPasswordRequest): Promise<{ success: boolean; userId?: string; error?: string }> => {
    try {
      const response = await forgotPasswordService.verifyEmail(data);
      return { success: true, userId: response.data?.user_id };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error?.message || 'Email verification failed',
      };
    }
  },

  handleResetPassword: async (userId: string, data: ResetPasswordRequest): Promise<{ success: boolean; error?: string }> => {
    try {
      await forgotPasswordService.resetPassword(userId, data);
      return { success: true };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error?.message || 'Password reset failed',
      };
    }
  },
};
