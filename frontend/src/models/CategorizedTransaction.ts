export interface CategorizedTransaction {
  transaction_id: string;
  date: string;
  description: string;
  merchant: string | null;
  category: string;
  confidence: number;
  method: string;
  rule_prediction: string | null;
  ml_prediction: string | null;
  debit: number | null;
  credit: number | null;
}

export interface CategorizationResponse {
  success: boolean;
  message: string;
  count: number;
  error?: string;
}

export interface CategorizedDataResponse {
  success: boolean;
  count: number;
  data: CategorizedTransaction[];
  error?: string;
}

export const CATEGORIES = [
  'Food',
  'Shopping',
  'Travel',
  'Bills',
  'Entertainment',
  'Subscriptions',
  'Health',
  'Groceries',
  'Education',
  'Fuel',
  'ATM',
  'Salary',
  'Interest',
  'Refund',
  'Internal_Transfer',
  'Person',
  'Other'
] as const;

export type Category = typeof CATEGORIES[number];
