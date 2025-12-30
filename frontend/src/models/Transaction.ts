export interface Transaction {
  transaction_id: string;
  date: string;
  description: string;
  debit: number | null;
  credit: number | null;
  balance: number | null;
  merchant: string | null;
  is_repaired: boolean;
}

export interface TransactionPreview {
  row_number: number;
  date: string;
  description: string;
  debit: number | null;
  credit: number | null;
  balance: number | null;
  errors?: string[];
}

export interface PreviewResponse {
  total: number;
  valid: number;
  rejected: number;
  preview: TransactionPreview[];
  rejected_rows: TransactionPreview[];
}

export interface ImportResponse {
  success: boolean;
  message: string;
  count: number;
  error?: string;
}
