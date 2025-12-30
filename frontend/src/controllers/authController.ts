import { authService, LoginCredentials, SignupCredentials } from '../services/authService';
import { useAuthStore } from '../store/authStore';

export interface ValidationErrors {
  firstName?: string;
  lastName?: string;
  username?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
}

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
const USERNAME_REGEX = /^[a-zA-Z0-9_]{3,20}$/;

export const authController = {
  validateLogin: (username: string, password: string): ValidationErrors => {
    const errors: ValidationErrors = {};

    if (!username.trim()) {
      errors.username = 'Username is required';
    } else if (!USERNAME_REGEX.test(username)) {
      errors.username = 'Username must be 3-20 characters and contain only letters, numbers, and underscores';
    }

    if (!password.trim()) errors.password = 'Password is required';

    return errors;
  },

  validateSignup: (firstName: string, lastName: string, username: string, email: string, password: string, confirmPassword: string): ValidationErrors => {
    const errors: ValidationErrors = {};

    if (!firstName.trim()) {
      errors.firstName = 'First name is required';
    }

    if (!lastName.trim()) {
      errors.lastName = 'Last name is required';
    }

    if (!username.trim()) {
      errors.username = 'Username is required';
    } else if (!USERNAME_REGEX.test(username)) {
      errors.username = 'Username must be 3-20 characters and contain only letters, numbers, and underscores';
    }

    if (!email.trim()) {
      errors.email = 'Email is required';
    } else if (!EMAIL_REGEX.test(email)) {
      errors.email = 'Invalid email format';
    }

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

  handleLogin: async (credentials: LoginCredentials): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await authService.login(credentials);
      useAuthStore.getState().login(response.data.access_token, response.data.user);
      return { success: true };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error?.message || 'Login failed. Please try again.',
      };
    }
  },

  handleSignup: async (credentials: SignupCredentials): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await authService.signup(credentials);
      useAuthStore.getState().login(response.data.access_token, response.data.user);
      return { success: true };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error?.message || 'Signup failed. Please try again.',
      };
    }
  },
};
