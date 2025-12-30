import apiClient from '../utils/apiClient';

export const preprocessService = {
  preprocessCSV: async (file: File): Promise<Blob> => {
    const formData = new FormData();
    formData.append('csv_file', file);

    const response = await apiClient.post('/preprocess_csv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob',
    });

    return response.data;
  },
};
