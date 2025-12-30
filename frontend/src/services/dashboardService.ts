import apiClient from '../utils/apiClient';
import { CategorySpending, SpendingTrend } from '../models/DashboardData';

export const dashboardService = {
  getCategorySpending: async (): Promise<CategorySpending[]> => {
    const response = await apiClient.get('/api/dashboard/spending');
    return response.data.data;
  },

  getSpendingTrends: async (startDate?: string, endDate?: string): Promise<SpendingTrend[]> => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    const response = await apiClient.get(`/api/dashboard/trends?${params.toString()}`);
    return response.data.data;
  }
};
