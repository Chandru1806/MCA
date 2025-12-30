import apiClient from '../utils/apiClient';
import { PDFUploadResponse } from '../models/PDFUploadResponse';

export const pdfService = {
  uploadPDF: async (file: File, bank: string): Promise<PDFUploadResponse> => {
    const formData = new FormData();
    formData.append('pdf', file);
    formData.append('bank', bank);

    const response = await apiClient.post('/pdf/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data.data;
  },

  downloadCSV: (filename: string): string => {
    return `${apiClient.defaults.baseURL}/pdf/download/${filename}`;
  },
};
