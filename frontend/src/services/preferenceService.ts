import apiClient from '../utils/apiClient';
import { Preference, PreferenceFormData } from '../models/Preference';

export const preferenceService = {
  getPreferences: async (): Promise<Preference> => {
    const response = await apiClient.get('/preference');
    return response.data.data;
  },

  updatePreferences: async (data: PreferenceFormData): Promise<Preference> => {
    const response = await apiClient.put('/preference', data);
    return response.data.data;
  },
};
