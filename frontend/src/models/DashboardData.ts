export interface CategorySpending {
  category: string;
  total_amount: number;
  transaction_count: number;
}

export interface SpendingTrend {
  year: number;
  month: number;
  category: string;
  amount: number;
}

export interface DashboardSummary {
  total_debit: number;
  total_credit: number;
  balance: number;
  categories: CategorySpending[];
}
