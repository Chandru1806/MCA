import apiClient from '../utils/apiClient';
import { PreviewResponse, ImportResponse, Transaction } from '../models/Transaction';

export const transactionService = {
  previewTransactions: async (statementId: number): Promise<PreviewResponse> => {
    const response = await apiClient.get(`/api/transactions/preview/${statementId}`);
    return response.data.data;
  },

  importTransactions: async (statementId: number): Promise<ImportResponse> => {
    const response = await apiClient.post(`/api/transactions/import/${statementId}`);
    return response.data;
  },

  getTransactions: async (statementId: number): Promise<Transaction[]> => {
    const response = await apiClient.get(`/api/transactions/${statementId}`);
    return response.data.transactions;
  }
};
