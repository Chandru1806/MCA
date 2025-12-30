import apiClient from '../utils/apiClient';
import { BudgetRequest, ForecastResponse } from '../models/AnalyticsData';

export const analyticsService = {
  generateForecast: async (request: BudgetRequest): Promise<ForecastResponse> => {
    const response = await apiClient.post('/api/analytics/forecast', request);
    return response.data;
  }
};
