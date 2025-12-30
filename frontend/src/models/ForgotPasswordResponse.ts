export interface ForgotPasswordResponse {
  success: boolean;
  message: string;
  data?: {
    user_id: string;
  };
}
