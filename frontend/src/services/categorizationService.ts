import apiClient from '../utils/apiClient';
import { CategorizationResponse, CategorizedDataResponse, CategorizedTransaction } from '../models/CategorizedTransaction';

export const categorizationService = {
  categorizeTransactions: async (statementId: number): Promise<CategorizationResponse> => {
    const response = await apiClient.post(`/api/categorization/categorize/${statementId}`);
    return response.data;
  },

  getCategorizedTransactions: async (statementId: number): Promise<CategorizedTransaction[]> => {
    const response = await apiClient.get(`/api/categorization/categories/${statementId}`);
    return response.data.data;
  },

  updateCategory: async (transactionId: string, category: string): Promise<void> => {
    await apiClient.put(`/api/categorization/update/${transactionId}`, { category });
  }
};
