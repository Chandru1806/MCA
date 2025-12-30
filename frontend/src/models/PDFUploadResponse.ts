export interface PDFUploadResponse {
  statement_id: string;
  bank_name: string;
  transaction_count: number;
  csv_filename?: string;
}
