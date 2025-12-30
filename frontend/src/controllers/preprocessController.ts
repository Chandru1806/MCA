import { preprocessService } from '../services/preprocessService';

export const preprocessController = {
  validateFile: (file: File): { valid: boolean; error?: string } => {
    if (!file.name.endsWith('.csv')) {
      return { valid: false, error: 'Only CSV files are allowed' };
    }
    if (file.size > 10 * 1024 * 1024) {
      return { valid: false, error: 'File size must be less than 10MB' };
    }
    return { valid: true };
  },

  processCSV: async (file: File): Promise<Blob> => {
    return await preprocessService.preprocessCSV(file);
  },

  downloadFile: (blob: Blob, originalFileName: string) => {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = originalFileName.replace('.csv', '_NORMALIZED.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  },
};
