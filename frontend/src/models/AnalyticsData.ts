export interface BudgetRequest {
  budget_limit: number;
  target_month: string;
  categories: string[];
  save_budget?: boolean;
}

export interface SavingsReport {
  category: string;
  current_spending: number;
  budget_limit: number;
  savings: number;
  message: string;
}

export interface ForecastResponse {
  success: boolean;
  data: SavingsReport[];
  budget_saved?: boolean;
}
