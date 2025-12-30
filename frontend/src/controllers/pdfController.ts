import { pdfService } from '../services/pdfService';
import { PDFUploadResponse } from '../models/PDFUploadResponse';

export const pdfController = {
  handleUpload: async (
    file: File,
    bank: string,
    onProgress: (progress: number) => void
  ): Promise<PDFUploadResponse> => {
    onProgress(30);
    const result = await pdfService.uploadPDF(file, bank);
    onProgress(100);
    return result;
  },

  validateFile: (file: File | null): string | null => {
    if (!file) return 'Please select a file';
    if (file.type !== 'application/pdf') return 'Only PDF files are allowed';
    if (file.size > 10 * 1024 * 1024) return 'File size must be less than 10MB';
    return null;
  },

  validateBank: (bank: string): string | null => {
    const validBanks = ['HDFC', 'KOTAK', 'SBI', 'ICICI', 'AXIS', 'CUB', 'IDFC'];
    if (!bank || bank === 'AUTO') return 'Please select a bank';
    if (!validBanks.includes(bank)) return 'Invalid bank selection';
    return null;
  },
};
