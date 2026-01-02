import apiClient from '../utils/apiClient';
import { Preference, PreferenceFormData } from '../models/Preference';

export const preferenceService = {
  getPreferences: async (): Promise<Preference> => {
    const response = await apiClient.get('/api/preference');
    return response.data.data;
  },

  updatePreferences: async (data: PreferenceFormData): Promise<Preference> => {
    const response = await apiClient.put('/api/preference', data);
    return response.data.data;
  },
};
